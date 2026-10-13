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
from demandes.serializers import DemandeSerializer, SollicitationSerializer, DonneurStructureSerializer
from participations.models import Participation
from accounts.models import ProfilDonneur
from django.db.models import Sum
        # 8. Générer les recommandations IA
from .utils import generer_recommandations_predictions
from demandes.management.commands.expirer_demandes import executer_expiration_demandes



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
                # Expirer les demandes dépassées avant d'afficher le suivi
        executer_expiration_demandes()

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
                "ville": {
                    "id": profil.ville.id,
                    "nom": profil.ville.nom,
                    "region": profil.ville.region.nom,
                } if profil.ville else None,
                "latitude": profil.latitude,
                "longitude": profil.longitude,
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

        executer_expiration_demandes()

        profil = request.user.profil_structure

        # 2. Compteurs sur les demandes
        demandes_actives = Demande.objects.filter(
            structure=profil,
            statut=Demande.StatutDemande.EN_COURS,
        ).count()

        demandes_terminees = Demande.objects.filter(
            structure=profil,
            statut=Demande.StatutDemande.TERMINEE,
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
                "ville": {
                    "id": profil.ville.id,
                    "nom": profil.ville.nom,
                    "region": profil.ville.region.nom,
                } if profil.ville else None,
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

# ===================================================
# Vue : liste des donneurs d'une structure
# ===================================================

@extend_schema(responses=DonneurStructureSerializer(many=True))
class StructureDonneursView(APIView):
    """
    GET /api/structure/donneurs/

    Renvoie la liste des donneurs qui ont interagi avec la structure
    connectée (via une sollicitation ou une participation).

    Chaque donneur est renvoyé avec :
      - ses infos (nom, prénom, groupe, ville, téléphone)
      - le nombre de sollicitations reçues
      - le nombre de participations confirmées
      - la date de la dernière interaction
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

        # 2. Récupérer tous les donneurs qui ont interagi avec cette structure.
        #    On part des sollicitations liées aux demandes de cette structure,
        #    et on récupère les donneurs uniques.
        donneurs_ids = (
            Sollicitation.objects
            .filter(demande__structure=profil)
            .values_list('donneur_id', flat=True)
            .distinct()
        )

        donneurs = ProfilDonneur.objects.filter(id__in=donneurs_ids)

        # 3. Pour chaque donneur, calculer les compteurs et la dernière interaction
        resultats = []
        for donneur in donneurs:
            # Sollicitations de ce donneur pour cette structure
            sollicitations = Sollicitation.objects.filter(
                donneur=donneur,
                demande__structure=profil,
            )

            nombre_sollicitations = sollicitations.count()

            # Participations confirmées de ce donneur pour cette structure
            nombre_participations = Participation.objects.filter(
                sollicitation__donneur=donneur,
                sollicitation__demande__structure=profil,
                statut=Participation.Statut.CONFIRMEE,
            ).count()

            # Dernière interaction : date de la dernière sollicitation
            derniere_sollicitation = sollicitations.order_by('-date_creation').first()
            derniere_interaction = (
                derniere_sollicitation.date_creation if derniere_sollicitation else None
            )

            # Initiales
            initiales = (
                (donneur.prenom or '')[:1] + (donneur.nom or '')[:1]
            ).upper() or '?'

            resultats.append({
                'id': donneur.id,
                'nom': donneur.nom,
                'prenom': donneur.prenom,
                'groupe_sanguin': donneur.groupe_sanguin,
                'ville': donneur.ville.nom if donneur.ville else '—',
                'region': donneur.ville.region.nom if donneur.ville else '—',
                'telephone': donneur.telephone,
                'initiales': initiales,
                'nombre_sollicitations': nombre_sollicitations,
                'nombre_participations': nombre_participations,
                'derniere_interaction': derniere_interaction,
            })

        # 4. Trier par date de dernière interaction décroissante
        resultats.sort(
            key=lambda x: x['derniere_interaction'] or timezone.datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )

        # 5. Sérialiser et renvoyer
        serializer = DonneurStructureSerializer(resultats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
# ===================================================
# Vue : prédictions et analyse pour une structure
# ===================================================

@extend_schema(responses=None)
class PredictionsStructureView(APIView):
    """
    GET /api/dashboard/structure/predictions/

    Analyse les données actuelles pour suggérer des zones à cibler.
    Basé sur :
      - Les demandes de la structure
      - Les donneurs disponibles par région
      - Les groupes sanguins les plus demandés

    Renvoie :
      - stats_globales : chiffres clés
      - par_region : demandes vs donneurs par région
      - par_groupe : demandes vs donneurs par groupe sanguin
      - zones_critiques : régions où il y a un déficit
      - recommandations_ia : texte généré par Groq (ou None)
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

        # 2. Récupérer les demandes de la structure
        demandes = Demande.objects.filter(structure=profil)

        # 3. Stats globales
        total_demandes = demandes.count()
        total_dons = Participation.objects.filter(
            sollicitation__demande__structure=profil,
            statut=Participation.Statut.CONFIRMEE,
        ).count()

        total_poches_demandees = demandes.aggregate(
            total=Sum('quantite')
        )['total'] or 0

        taux_satisfaction = (
            round((total_dons / total_poches_demandees) * 100)
            if total_poches_demandees > 0 else 0
        )

        # 4. Analyse par région
        par_region = []

        regions_concernees = demandes.values_list(
            'ville__region__nom', flat=True
        ).distinct()

        for region_nom in regions_concernees:
            demandes_region = demandes.filter(ville__region__nom=region_nom)

            donneurs_region = ProfilDonneur.objects.filter(
                ville__region__nom=region_nom,
                disponible=True,
            )

            nb_demandes = demandes_region.count()
            nb_donneurs = donneurs_region.count()

            ratio = round(nb_demandes / nb_donneurs, 2) if nb_donneurs > 0 else None

            par_region.append({
                "region": region_nom,
                "demandes": nb_demandes,
                "donneurs_disponibles": nb_donneurs,
                "ratio": ratio,
            })

        par_region.sort(
            key=lambda x: x['ratio'] if x['ratio'] is not None else 999,
            reverse=True,
        )

        # 5. Analyse par groupe sanguin
        par_groupe = []

        groupes_demandes = demandes.values_list(
            'groupe_sanguin', flat=True
        ).distinct()

        for groupe in groupes_demandes:
            nb_demandes = demandes.filter(groupe_sanguin=groupe).count()
            nb_donneurs = ProfilDonneur.objects.filter(
                groupe_sanguin=groupe,
                disponible=True,
            ).count()

            par_groupe.append({
                "groupe": groupe,
                "demandes": nb_demandes,
                "donneurs": nb_donneurs,
                "alerte": nb_donneurs < nb_demandes,
            })

        par_groupe.sort(key=lambda x: x['demandes'], reverse=True)

        # 6. Zones critiques
        zones_critiques = []

        for item in par_region:
            if item['donneurs_disponibles'] == 0:
                zones_critiques.append({
                    "region": item['region'],
                    "raison": "Aucun donneur disponible dans cette région.",
                    "demandes": item['demandes'],
                })
            elif item['ratio'] and item['ratio'] > 3:
                zones_critiques.append({
                    "region": item['region'],
                    "raison": f"Ratio élevé : {item['ratio']} demandes par donneur.",
                    "demandes": item['demandes'],
                })

        # 7. Construire le dict de stats
        stats = {
            "stats_globales": {
                "total_demandes": total_demandes,
                "total_dons": total_dons,
                "taux_satisfaction": taux_satisfaction,
            },
            "par_region": par_region,
            "par_groupe": par_groupe,
            "zones_critiques": zones_critiques,
        }

        recommandations = generer_recommandations_predictions(stats)

        # 9. Réponse finale
        return Response({
            **stats,
            "recommandations_ia": recommandations,
        }, status=status.HTTP_200_OK)