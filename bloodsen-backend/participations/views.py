from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from demandes.models import Sollicitation      # ← import autorisé (sens demandes → participations)
from participations.models import Participation     
from .services import confirmer_participation
from .serializers import ParticipationSerializer, SollicitationStructureSerializer


@extend_schema(request=None)
class ConfirmerParticipationView(APIView):
    """
    POST /api/sollicitations/<id>/confirmer/

    Appelée par la STRUCTURE (pas le donneur) pour confirmer
    que le donneur s'est bien présenté et a fait le don.

    Crée une Participation liée à la sollicitation.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # 1. Récupérer la sollicitation
        sollicitation = get_object_or_404(Sollicitation, pk=pk)

        # 2. Vérifier que l'utilisateur est bien une structure
        if request.user.role != 'structure':
            return Response(
                {"detail": "Seule une structure peut confirmer une participation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 3. Vérifier que la structure est bien propriétaire de la demande
        if sollicitation.demande.structure != request.user.profil_structure:
            return Response(
                {"detail": "Cette sollicitation ne concerne pas une de vos demandes."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 4. Vérifier que la sollicitation est bien au statut "acceptee"
        if sollicitation.statut != Sollicitation.Statut.ACCEPTEE:
            return Response(
                {"detail": f"Impossible de confirmer : la sollicitation est au statut '{sollicitation.statut}' (il faut qu'elle soit 'acceptee')."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 5. Vérifier qu'une participation n'existe pas déjà
        #    (relation OneToOne avec related_name='participation')
        if hasattr(sollicitation, 'participation'):
            return Response(
                {"detail": "Une participation existe déjà pour cette sollicitation."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 6. Appeler le service qui :
        #    - crée la Participation
        #    - ajoute 100 points au donneur
        #    - termine la demande si elle est satisfaite
        participation = confirmer_participation(sollicitation)

        # 7. Renvoyer la participation créée
        serializer = ParticipationSerializer(participation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ===================================================
# Vue : lister les participations du donneur connecté
# ===================================================

@extend_schema(responses=ParticipationSerializer(many=True))
class MesParticipationsView(APIView):
    """
    GET /api/participations/

    Renvoie l'historique des dons confirmés du donneur connecté,
    triés par date de confirmation décroissante (les plus récents en haut).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. Vérifier le rôle
        if request.user.role != 'donneur':
            return Response(
                {"detail": "Seul un donneur peut consulter son historique."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 2. Récupérer les participations du donneur connecté.
        #    Attention : on doit traverser la relation Sollicitation
        #    pour atteindre le donneur (d'où le "sollicitation__donneur").
        participations = Participation.objects.filter(
            sollicitation__donneur=request.user.profil_donneur,
            statut=Participation.Statut.CONFIRMEE,   # uniquement les dons effectifs
        ).order_by('-date_confirmation')

        # 3. Sérialiser et renvoyer
        serializer = ParticipationSerializer(participations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ===================================================
# Vue : liste des participations/sollicitations d'une structure
# ===================================================

@extend_schema(responses=SollicitationStructureSerializer(many=True))
class StructureParticipationsView(APIView):
    """
    GET /api/structure/participations/

    Renvoie toutes les sollicitations liées aux demandes de la structure
    connectée, avec leur statut combiné (pending, confirmed, etc.).

    Cette vue mélange volontairement les sollicitations et les
    participations pour que la structure voie tout le cycle :
      - sollicitations en attente
      - sollicitations acceptées (donneur prêt à venir)
      - participations confirmées (don effectué)
      - sollicitations refusées
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. Vérifier le rôle
        if request.user.role != 'structure':
            return Response(
                {"detail": "Cet endpoint est réservé aux structures."},
                status=status.HTTP_403_FORBIDDEN,
            )

        profil = request.user.profil_structure

        # 2. Récupérer toutes les sollicitations liées aux demandes
        #    de cette structure, avec les relations préchargées.
        sollicitations = (
            Sollicitation.objects
            .filter(demande__structure=profil)
            .select_related(
                'donneur',
                'demande',
                'demande__structure',
                'participation',
            )
            .order_by('-date_creation')
        )

        # 3. Sérialiser et renvoyer
        serializer = SollicitationStructureSerializer(sollicitations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)