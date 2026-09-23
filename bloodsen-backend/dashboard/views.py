from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from collections import Counter

from datetime import timedelta
from django.utils import timezone
from django.db.models import Count


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

        sollicitations_acceptees = Sollicitation.objects.filter(
            donneur=profil,
            statut=Sollicitation.Statut.ACCEPTEE,
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
                "sollicitations_acceptees": sollicitations_acceptees,
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


# ===================================================
# Vue : statistiques agrégées pour le dashboard structure
# ===================================================

@extend_schema(responses=None)
class StatsStructureView(APIView):
    """
    GET /api/dashboard/structure/stats/

    Renvoie les statistiques agrégées pour le tableau de bord
    d'une structure :
      - chart_semaine : nombre de demandes créées chaque jour sur 7 jours
      - repartition_groupes : participations confirmées par groupe sanguin
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
        aujourd_hui = timezone.now().date()
        il_y_a_7_jours = aujourd_hui - timedelta(days=6)

        # ==========================================
        # CHART HEBDOMADAIRE
        # ==========================================
        # Pour chaque jour des 7 derniers jours, on compte
        # les demandes créées par cette structure.

        # On récupère toutes les demandes créées dans la période
        demandes_periode = Demande.objects.filter(
            structure=profil,
            date_creation__date__gte=il_y_a_7_jours,
            date_creation__date__lte=aujourd_hui,
        ).values_list('date_creation__date', flat=True)

        # On compte par date
        compteur_par_date = Counter(demandes_periode)

        # On construit les 7 jours
        jours_fr = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
        chart_semaine = []
        for i in range(7):
            jour = il_y_a_7_jours + timedelta(days=i)
            nom_jour = jours_fr[jour.weekday()]
            valeur = compteur_par_date.get(jour, 0)
            chart_semaine.append({
                "jour": nom_jour,
                "date": jour.isoformat(),
                "valeur": valeur,
            })

        # ==========================================
        # RÉPARTITION PAR GROUPE SANGUIN
        # ==========================================
        # On compte les participations confirmées par groupe sanguin
        # pour toutes les demandes de cette structure.

        repartition_qs = (
            Participation.objects
            .filter(
                sollicitation__demande__structure=profil,
                statut=Participation.Statut.CONFIRMEE,
            )
            .values('sollicitation__demande__groupe_sanguin')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        total_dons = sum(item['total'] for item in repartition_qs) or 1  # évite division par 0

        repartition_groupes = []
        for item in repartition_qs:
            groupe = item['sollicitation__demande__groupe_sanguin']
            total = item['total']
            pourcentage = round((total / total_dons) * 100)
            repartition_groupes.append({
                "groupe": groupe,
                "dons": total,
                "pourcentage": pourcentage,
            })

        return Response({
            "chart_semaine": chart_semaine,
            "repartition_groupes": repartition_groupes,
        }, status=status.HTTP_200_OK)