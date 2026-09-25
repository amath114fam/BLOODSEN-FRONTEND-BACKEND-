from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction   # ← à ajouter si pas déjà présent

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter


from .models import Demande, Sollicitation
from .serializers import DemandeCreateSerializer, DemandeSerializer, SollicitationSerializer
from .services import creer_sollicitations_pour_demande



# ============================================================
# Vue helper : logique commune pour accepter/refuser
# ============================================================

class _RepondreSollicitationView(APIView):
    """
    Classe de base (non exposée directement) qui contient la logique
    partagée entre "accepter" et "refuser" une sollicitation.

    Les sous-classes définissent juste le nouveau statut à appliquer.
    """

    permission_classes = [IsAuthenticated]

    # À redéfinir dans les sous-classes
    nouveau_statut = None

    def post(self, request, pk):
        # 1. Récupérer la sollicitation (404 si elle n'existe pas)
        sollicitation = get_object_or_404(Sollicitation, pk=pk)

        # 2. Vérifier que l'utilisateur est bien un donneur
        if request.user.role != 'donneur':
            return Response(
                {"detail": "Seul un donneur peut répondre à une sollicitation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 3. Vérifier que la sollicitation appartient bien à CE donneur
        #    (request.user.profil_donneur est accessible grâce au OneToOne)
        if sollicitation.donneur != request.user.profil_donneur:
            return Response(
                {"detail": "Cette sollicitation ne vous est pas adressée."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 4. Vérifier que la sollicitation est encore en attente
        #    (on ne peut pas accepter ce qui a déjà été traité)
        if sollicitation.statut != Sollicitation.Statut.EN_ATTENTE:
            return Response(
                {"detail": f"Cette sollicitation a déjà été traitée (statut actuel : {sollicitation.statut})."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 5. Appliquer le nouveau statut
        sollicitation.statut = self.nouveau_statut
        sollicitation.date_reponse = timezone.now()
        sollicitation.save()

        # 6. Renvoyer la sollicitation mise à jour
        serializer = SollicitationSerializer(sollicitation)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccepterSollicitationView(_RepondreSollicitationView):
    """POST /api/sollicitations/<id>/accepter/"""
    nouveau_statut = Sollicitation.Statut.ACCEPTEE


class RefuserSollicitationView(_RepondreSollicitationView):
    """POST /api/sollicitations/<id>/refuser/"""
    nouveau_statut = Sollicitation.Statut.REFUSEE


# ============================================================
# Vue : créer une demande (déclenche le matching automatique)
# ============================================================
@extend_schema(request=DemandeCreateSerializer)
class CreerDemandeView(APIView):
    """
    POST /api/demandes/

    Crée une demande de sang ET génère automatiquement les sollicitations
    pour tous les donneurs compatibles.

    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 1. Vérifier que l'utilisateur est bien une structure
        if request.user.role != 'structure':
            return Response(
                {"detail": "Seule une structure de santé peut créer une demande."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 2. Valider les données envoyées
        serializer = DemandeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 3. Créer la Demande.
        #    serializer.save() appelle la méthode create() du serializer,
        #    MAIS on lui passe un argument supplémentaire "structure" qui
        #    n'est PAS dans les données du formulaire (il vient de
        #    l'utilisateur connecté, pas du JSON).
        demande = serializer.save(structure=request.user.profil_structure)

        # 4. Lancer le matching : créer les sollicitations pour cette demande.
        #    On importe ici plutôt qu'en haut du fichier pour éviter un import
        #    circulaire potentiel entre views.py et services.py.
        sollicitations = creer_sollicitations_pour_demande(demande)

        # 5. Renvoyer la demande créée.
        #    On renvoie aussi le nombre de sollicitations générées pour que
        #    le frontend puisse afficher "X donneurs ont été sollicités".
        response_serializer = DemandeSerializer(demande)
        return Response(
            {
                **response_serializer.data,
                "sollicitations_creees": len(sollicitations),
            },
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# Vue : lister les demandes de la structure connectée
# ============================================================

class ListeDemandesView(APIView):
    """
    GET /api/demandes/

    Renvoie toutes les demandes créées par la structure actuellement
    connectée. Une structure ne voit QUE ses propres demandes.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. Vérifier le rôle
        if request.user.role != 'structure':
            return Response(
                {"detail": "Seule une structure peut consulter cette liste."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 2. Récupérer les demandes de la structure connectée,
        #    triées par date de création décroissante (les plus récentes d'abord).
        demandes = Demande.objects.filter(
            structure=request.user.profil_structure
        ).order_by('-date_creation')

        # 3. Sérialiser et renvoyer la liste.
        #    many=True dit au serializer qu'on lui passe une LISTE d'objets,
        #    pas un seul objet.
        serializer = DemandeSerializer(demandes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ===================================================
# Vue : lister les sollicitations du donneur connecté
# ===================================================

@extend_schema(
    parameters=[
        OpenApiParameter(
            name='statut',
            description="Filtrer par statut de sollicitation (en_attente, acceptee, refusee, expiree)",
            required=False,
            type=str,
            enum=['en_attente', 'acceptee', 'refusee', 'expiree'],
        ),
    ],
    responses=SollicitationSerializer(many=True),
)
class MesSollicitationsView(APIView):
    """
    GET /api/sollicitations/

    Renvoie toutes les sollicitations reçues par le donneur connecté,
    triées par date de création décroissante (les plus récentes en haut,
    comme dans une boîte mail).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. Vérifier le rôle
        if request.user.role != 'donneur':
            return Response(
                {"detail": "Seul un donneur peut consulter ses sollicitations."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 2. Construire le queryset de base (toutes les sollicitations du donneur)
        sollicitations = Sollicitation.objects.filter(
            donneur=request.user.profil_donneur
        )

        # 3. Filtre optionnel sur le statut.
        #    On lit le paramètre ?statut=... s'il est fourni.
        statut = request.query_params.get('statut')
        if statut:
            sollicitations = sollicitations.filter(statut=statut)

        # 4. Trier par date décroissante
        sollicitations = sollicitations.order_by('-date_creation')

        # 5. Sérialiser et renvoyer
        serializer = SollicitationSerializer(sollicitations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ===================================================
# Vue : annuler une demande
# ===================================================

@extend_schema(request=None)
class AnnulerDemandeView(APIView):
    """
    POST /api/demandes/<id>/annuler/

    Permet à une structure d'annuler une de ses propres demandes
    tant qu'elle est encore "en_cours".

    Effets de bord :
      - Toutes les sollicitations "en_attente" liées passent à "expiree"
        (elles n'ont plus de sens puisque la demande est annulée)
      - Les sollicitations déjà traitées (acceptee / refusee) ne changent pas
        (elles restent dans l'historique)
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # 1. Récupérer la demande
        demande = get_object_or_404(Demande, pk=pk)

        # 2. Vérifier que l'utilisateur est bien une structure
        if request.user.role != 'structure':
            return Response(
                {"detail": "Seule une structure peut annuler une demande."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 3. Vérifier que la structure est bien propriétaire
        if demande.structure != request.user.profil_structure:
            return Response(
                {"detail": "Cette demande ne vous appartient pas."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 4. Vérifier que la demande est encore "en_cours"
        if demande.statut != Demande.Statut.EN_COURS:
            return Response(
                {"detail": f"Impossible d'annuler : la demande est déjà au statut '{demande.statut}'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 5. Tout se passe dans une transaction : soit tout réussit, soit rien
        with transaction.atomic():
            # 5a. Marquer les sollicitations "en_attente" comme "expiree"
            Sollicitation.objects.filter(
                demande=demande,
                statut=Sollicitation.Statut.EN_ATTENTE,
            ).update(statut=Sollicitation.Statut.EXPIREE)

            # 5b. Passer la demande à "annulee"
            demande.statut = Demande.Statut.ANNULEE
            demande.save(update_fields=['statut'])

        # 6. Renvoyer la demande mise à jour
        serializer = DemandeSerializer(demande)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ===================================================
# Vue : détail d'une demande
# ===================================================

@extend_schema(responses=DemandeSerializer)
class DetailDemandeView(APIView):
    """
    GET /api/demandes/<id>/

    Renvoie le détail d'une demande précise. Seule la structure
    propriétaire peut y accéder (les autres structures et les
    donneurs sont refusés).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # 1. Récupérer la demande
        demande = get_object_or_404(Demande, pk=pk)

        # 2. Vérifier que l'utilisateur est bien une structure
        if request.user.role != 'structure':
            return Response(
                {"detail": "Seule une structure peut consulter une demande."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 3. Vérifier que la structure est bien propriétaire
        if demande.structure != request.user.profil_structure:
            return Response(
                {"detail": "Cette demande ne vous appartient pas."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 4. Sérialiser et renvoyer
        serializer = DemandeSerializer(demande)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ===================================================
# Vue : détail d'une sollicitation
# ===================================================

@extend_schema(responses=SollicitationSerializer)
class DetailSollicitationView(APIView):
    """
    GET /api/sollicitations/<id>/

    Renvoie le détail d'une sollicitation précise.
    Seul le donneur concerné peut y accéder.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # 1. Récupérer la sollicitation
        sollicitation = get_object_or_404(Sollicitation, pk=pk)

        # 2. Vérifier que l'utilisateur est bien un donneur
        if request.user.role != 'donneur':
            return Response(
                {"detail": "Seul un donneur peut consulter le détail d'une sollicitation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 3. Vérifier que la sollicitation appartient bien à ce donneur
        if sollicitation.donneur != request.user.profil_donneur:
            return Response(
                {"detail": "Cette sollicitation ne vous est pas adressée."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 4. Sérialiser et renvoyer
        serializer = SollicitationSerializer(sollicitation)
        return Response(serializer.data, status=status.HTTP_200_OK)