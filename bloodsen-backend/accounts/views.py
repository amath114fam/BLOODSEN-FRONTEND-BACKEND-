from django.db import transaction
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from .models import Utilisateur, InscriptionEnAttente, ProfilDonneur, ProfilStructureSante
from .serializers import (
    InscriptionDonneurSerializer,
    InscriptionStructureSerializer,
    VerificationTokenSerializer,
    EmailTokenObtainPairSerializer,
    ModifierProfilDonneurSerializer,
    ModifierProfilStructureSerializer,
    ChangerMotDePasseSerializer, 
)
from .utils import envoyer_email_verification


# ============================================================
# VUE 1 : Inscription d'un donneur
# ============================================================

class InscrireDonneurView(generics.GenericAPIView):
    """
    POST /api/auth/inscription/donneur/

    Reçoit les infos du formulaire donneur, les valide, puis crée une
    InscriptionEnAttente (PAS un Utilisateur) et envoie l'email de
    vérification contenant le lien avec le token.
    """

    serializer_class = InscriptionDonneurSerializer

    # AllowAny : cette route est accessible sans être connecté
    # (c'est justement le but : s'inscrire avant d'avoir un compte !)
    permission_classes = [AllowAny]

    def post(self, request):
        # 1. On passe les données reçues au serializer pour validation.
        #    is_valid(raise_exception=True) : si les données sont invalides,
        #    DRF renvoie automatiquement une erreur 400 avec les détails.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. serializer.save() appelle la méthode create() du serializer,
        #    qui crée une InscriptionEnAttente et nous la renvoie.
        inscription = serializer.save()

        # 3. On envoie l'email de vérification avec le token généré.
        envoyer_email_verification(inscription.email, inscription.token)

        # 4. On renvoie une réponse de succès (201 Created).
        #    On ne renvoie PAS l'objet InscriptionEnAttente : ce serait
        #    une fuite d'information inutile (et potentiellement le hash
        #    du mot de passe, qu'on ne veut jamais exposer).
        return Response(
            {"message": "Un email de vérification a été envoyé à votre adresse."},
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# VUE 2 : Inscription d'une structure de santé
# ============================================================

class InscrireStructureView(generics.GenericAPIView):
    """
    POST /api/auth/inscription/structure/

    Exactement la même logique que pour le donneur, avec un serializer
    différent (qui contient les champs propres à une structure).
    """

    serializer_class = InscriptionStructureSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        inscription = serializer.save()
        envoyer_email_verification(inscription.email, inscription.token)

        return Response(
            {"message": "Un email de vérification a été envoyé à votre adresse."},
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# VUE 3 : Vérification de l'email (création réelle du compte)
# ============================================================
@extend_schema(request=VerificationTokenSerializer)
class VerifierEmailView(APIView):
    """
    POST /api/auth/verifier-email/
    Body attendu : { "token": "xxx" }

    C'est ICI que le vrai Utilisateur est créé en base, ainsi que
    son profil (donneur ou structure). Tant que cette vue n'est pas
    appelée avec un token valide, rien n'existe dans Utilisateur.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        # 1. On valide la forme de la requête (le champ "token" est
        #    obligatoire et doit être une chaîne).
        serializer = VerificationTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']

        # 2. On cherche l'inscription en attente correspondant au token.
        #    Si elle n'existe pas (mauvais token ou déjà utilisé), erreur 400.
        try:
            inscription = InscriptionEnAttente.objects.get(token=token)
        except InscriptionEnAttente.DoesNotExist:
            return Response(
                {"detail": "Lien de vérification invalide ou déjà utilisé."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 3. On vérifie que le lien n'a pas expiré (24h dans notre cas).
        if inscription.est_expire():
            inscription.delete()  # on nettoie la demande expirée
            return Response(
                {"detail": "Ce lien de vérification a expiré. Veuillez vous réinscrire."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 4. transaction.atomic() : tout ce qui est dans ce bloc
        #    réussit ensemble OU échoue ensemble. Si par exemple la
        #    création du Profil échoue, l'Utilisateur n'est pas créé
        #    non plus. Ça évite les "utilisateurs sans profil".
        with transaction.atomic():
            # 4a. On crée l'Utilisateur, en réutilisant le mot de passe
            #     DÉJÀ hashé stocké dans l'inscription en attente.
            #     On assigne directement .password (pas set_password()),
            #     sinon on re-hasherait un hash, ce qui casserait tout.
            utilisateur = Utilisateur(
                email=inscription.email,
                role=inscription.role,
            )
            utilisateur.password = inscription.mot_de_passe_hash
            utilisateur.save()

            # 4b. On crée le bon profil selon le rôle.
            donnees = inscription.donnees_profil

            if inscription.role == Utilisateur.Role.DONNEUR:
                ProfilDonneur.objects.create(utilisateur=utilisateur, **donnees)
            else:
                ProfilStructureSante.objects.create(utilisateur=utilisateur, **donnees)

            # 4c. On supprime la ligne temporaire : elle a fait son job.
            inscription.delete()

        # 5. L'utilisateur est maintenant actif. Pour lui éviter de
        #    devoir se reconnecter tout de suite, on lui délivre
        #    directement un token JWT valide (comme à la connexion).
        refresh = RefreshToken.for_user(utilisateur)

        return Response({
            "message": "Votre compte a été activé avec succès.",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)


# ============================================================
# VUE 4 : Connexion (avec JWT personnalisé)
# ============================================================
class EmailTokenObtainPairView(TokenObtainPairView):
    """
    POST /api/auth/connexion/
    Body attendu : { "email": "...", "password": "..." }

    On remplace juste le serializer par défaut par le nôtre,
    qui ajoute "role" et "email" dans le payload du token JWT.
    """

    serializer_class = EmailTokenObtainPairSerializer


# ============================================================
# VUE 5 : Récupérer les infos de l'utilisateur connecté
# ============================================================

class MoiView(APIView):
    """
    GET /api/auth/moi/

    Renvoie les infos de l'utilisateur connecté, plus son profil
    spécifique (donneur ou structure). Nécessite un token JWT valide
    dans le header : Authorization: Bearer <access_token>
    """

    # IsAuthenticated : Django refuse automatiquement la requête
    # avec un 401 si aucun token valide n'est fourni.
    permission_classes = [IsAuthenticated]

    def get(self, request):
        utilisateur = request.user

        # Infos communes à tous les utilisateurs, quel que soit le rôle.
        # On utilise un dictionnaire Python qui sera converti en JSON.
        data = {
            "id": utilisateur.id,
            "email": utilisateur.email,
            "role": utilisateur.role,
        }

        # Ensuite, selon le rôle, on ajoute le "profil" correspondant.
        if utilisateur.role == Utilisateur.Role.DONNEUR:
            profil = utilisateur.profil_donneur
            data["profil"] = {
                "nom": profil.nom,
                "prenom": profil.prenom,
                "telephone": profil.telephone,
                "groupe_sanguin": profil.groupe_sanguin,
                "region": profil.region,
                "ville": profil.ville,
                "quartier": profil.quartier,
                "disponible": profil.disponible,
                "points_total": profil.points_total,
            }

        elif utilisateur.role == Utilisateur.Role.STRUCTURE:
            profil = utilisateur.profil_structure
            data["profil"] = {
                "nom_structure": profil.nom_structure,
                "adresse": profil.adresse,
                "region": profil.region,
                "ville": profil.ville,
                "quartier": profil.quartier,
            }

        else:
            # Cas admin : pas de ProfilDonneur ni de ProfilStructureSante.
            # On renvoie explicitement profil = null pour que le frontend
            # ait toujours la clé "profil" dans la réponse.
            data["profil"] = None

        return Response(data)

    def patch(self, request):
        """
        PATCH : modification du profil (donneur OU structure).
        """
        role = request.user.role

        # ==========================================
        # CAS DONNEUR
        # ==========================================
        if role == 'donneur':
            profil = request.user.profil_donneur
            serializer = ModifierProfilDonneurSerializer(
                instance=profil,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            profil.refresh_from_db()

            return Response(
                {
                    "message": "Profil mis à jour avec succès.",
                    "profil": {
                        "nom": profil.nom,
                        "prenom": profil.prenom,
                        "telephone": profil.telephone,
                        "groupe_sanguin": profil.groupe_sanguin,
                        "region": profil.region,
                        "ville": profil.ville,
                        "quartier": profil.quartier,
                        "disponible": profil.disponible,
                    },
                },
                status=status.HTTP_200_OK,
            )

        # ==========================================
        # CAS STRUCTURE
        # ==========================================
        if role == 'structure':
            profil = request.user.profil_structure
            serializer = ModifierProfilStructureSerializer(
                instance=profil,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            profil.refresh_from_db()

            return Response(
                {
                    "message": "Profil mis à jour avec succès.",
                    "profil": {
                        "nom_structure": profil.nom_structure,
                        "adresse": profil.adresse,
                        "region": profil.region,
                        "ville": profil.ville,
                        "quartier": profil.quartier,
                    },
                },
                status=status.HTTP_200_OK,
            )

        # ==========================================
        # CAS NON SUPPORTÉ (admin)
        # ==========================================
        return Response(
            {"detail": "Ce type de compte ne peut pas modifier son profil via cet endpoint."},
            status=status.HTTP_403_FORBIDDEN,
        )

# ============================================================
# VUE 6 : Changement de mot de passe
# ============================================================

@extend_schema(
    request=ChangerMotDePasseSerializer,
    responses=None,
    description="Permet à un utilisateur connecté de changer son mot de passe.",
)
class ChangerMotDePasseView(APIView):
    """
    POST /api/auth/changer-mot-de-passe/

    Vérifie le mot de passe actuel avant d'accepter le nouveau.
    Accessible à tous les utilisateurs connectés (donneur + structure).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 1. Valider les données (le serializer vérifie le mot de passe actuel)
        serializer = ChangerMotDePasseSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)

        # 2. Sauvegarder le nouveau mot de passe
        serializer.save()

        # 3. Réponse de succès
        return Response(
            {"message": "Mot de passe mis à jour avec succès."},
            status=status.HTTP_200_OK,
        )