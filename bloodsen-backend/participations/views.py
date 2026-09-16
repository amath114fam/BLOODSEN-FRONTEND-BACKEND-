from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from demandes.models import Sollicitation      # ← import autorisé (sens demandes → participations)
from .models import Participation
from .serializers import ParticipationSerializer


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

        # 6. Créer la participation
        participation = Participation.objects.create(
            sollicitation=sollicitation,
            statut=Participation.Statut.CONFIRMEE,
        )

        # 7. Renvoyer la participation créée
        serializer = ParticipationSerializer(participation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)