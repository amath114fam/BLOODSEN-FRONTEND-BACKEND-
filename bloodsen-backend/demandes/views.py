from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

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

@extend_schema(responses=SollicitationSerializer(many=True))
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

        # 2. Récupérer les sollicitations du donneur connecté
        sollicitations = Sollicitation.objects.filter(
            donneur=request.user.profil_donneur
        ).order_by('-date_creation')  # le '-' = tri décroissant

        # 3. Sérialiser et renvoyer
        serializer = SollicitationSerializer(sollicitations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)