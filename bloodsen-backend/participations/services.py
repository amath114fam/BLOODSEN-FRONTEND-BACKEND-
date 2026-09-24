from django.db import transaction
from django.db.models import Sum
from .models import Participation


def confirmer_participation(sollicitation):
    POINTS_PAR_DON = 100

    with transaction.atomic():
        # 1. Créer la participation
        participation = Participation.objects.create(
            sollicitation=sollicitation,
            statut=Participation.Statut.CONFIRMEE,
        )

        # 2. RECALCULER les points (pas d'incrémentation)
        donneur = sollicitation.donneur
        nb_dons = Participation.objects.filter(
            sollicitation__donneur=donneur,
            statut=Participation.Statut.CONFIRMEE,
        ).count()
        donneur.points_total = nb_dons * POINTS_PAR_DON
        donneur.save(update_fields=['points_total'])

        # 3. Vérifier si la demande est satisfaite
        demande = sollicitation.demande
        total_poches = Participation.objects.filter(
            sollicitation__demande=demande,
            statut=Participation.Statut.CONFIRMEE,
        ).count()

        if total_poches >= demande.quantite:
            demande.statut = demande.Statut.TERMINEE
            demande.save(update_fields=['statut'])

        return participation