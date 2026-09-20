from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from demandes.models import Demande, Sollicitation
from demandes.serializers import DemandeSerializer, SollicitationSerializer
from participations.models import Participation


# ===================================================
# Vue : dashboard du donneur connecté
# ===================================================

@extend_schema(responses=None)
class DashboardDonneurView(APIView):
    """
    GET /api/dashboard/donneur/

    Agrège en un seul appel toutes les données dont le donneur
    a besoin pour afficher son tableau de bord :
      - ses infos de profil (nom, groupe sanguin, points)
      - compteurs (sollicitations en attente, dons effectués)
      - 3 dernières sollicitations reçues
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. Vérifier le rôle
        if request.user.role != 'donneur':
            return Response(
                {"detail": "Cet endpoint est réservé aux donneurs."},
                status=status.HTTP_403_FORBIDDEN,
            )

        profil = request.user.profil_donneur

        # 2. Compteurs
        sollicitations_en_attente = Sollicitation.objects.filter(
            donneur=profil,
            statut=Sollicitation.Statut.EN_ATTENTE,
        ).count()

        dons_effectues = Participation.objects.filter(
            sollicitation__donneur=profil,
            statut=Participation.Statut.CONFIRMEE,
        ).count()

        # 3. Les 3 dernières sollicitations reçues
        dernieres_sollicitations = Sollicitation.objects.filter(
            donneur=profil
        ).order_by('-date_creation')[:3]

        # 4. Assembler la réponse
        data = {
            "profil": {
                "nom": profil.nom,
                "prenom": profil.prenom,
                "groupe_sanguin": profil.groupe_sanguin,
                "region": profil.region,
                "ville": profil.ville,
                "disponible": profil.disponible,
                "points_total": profil.points_total,
            },
            "compteurs": {
                "sollicitations_en_attente": sollicitations_en_attente,
                "dons_effectues": dons_effectues,
            },
            "dernieres_sollicitations": SollicitationSerializer(
                dernieres_sollicitations, many=True
            ).data,
        }
        return Response(data, status=status.HTTP_200_OK)


# ===================================================
# Vue : dashboard de la structure connectée
# ===================================================

@extend_schema(responses=None)
class DashboardStructureView(APIView):
    """
    GET /api/dashboard/structure/

    Agrège en un seul appel toutes les données dont la structure
    a besoin pour afficher son tableau de bord :
      - ses infos de profil (nom, ville)
      - compteurs (demandes actives, terminées, sollicitations, dons)
      - 3 dernières demandes créées
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

        # 2. Compteurs sur les demandes
        demandes_actives = Demande.objects.filter(
            structure=profil,
            statut=Demande.Statut.EN_COURS,
        ).count()

        demandes_terminees = Demande.objects.filter(
            structure=profil,
            statut=Demande.Statut.TERMINEE,
        ).count()

        # 3. Compteurs sur les sollicitations et participations
        sollicitations_totales = Sollicitation.objects.filter(
            demande__structure=profil,
        ).count()

        participations_confirmees = Participation.objects.filter(
            sollicitation__demande__structure=profil,
            statut=Participation.Statut.CONFIRMEE,
        ).count()

        # 4. Les 3 dernières demandes créées
        dernieres_demandes = Demande.objects.filter(
            structure=profil
        ).order_by('-date_creation')[:3]

        # 5. Assembler la réponse
        data = {
            "profil": {
                "nom_structure": profil.nom_structure,
                "adresse": profil.adresse,
                "region": profil.region,
                "ville": profil.ville,
            },
            "compteurs": {
                "demandes_actives": demandes_actives,
                "demandes_terminees": demandes_terminees,
                "sollicitations_totales": sollicitations_totales,
                "participations_confirmees": participations_confirmees,
            },
            "dernieres_demandes": DemandeSerializer(
                dernieres_demandes, many=True
            ).data,
        }
        return Response(data, status=status.HTTP_200_OK)