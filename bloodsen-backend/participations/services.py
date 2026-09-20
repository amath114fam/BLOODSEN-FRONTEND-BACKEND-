from django.db import transaction
from django.db.models import Sum
from .models import Participation


def confirmer_participation(sollicitation):
    """
    Logique métier déclenchée quand une structure confirme
    qu'un donneur a effectivement donné son sang.

    Trois choses se passent :
      1. On crée la Participation (statut "confirmee")
      2. On ajoute 100 points au donneur
      3. On vérifie si la demande est maintenant satisfaite
         (= le nombre de participations confirmées atteint
         la quantité demandée), et si oui, on la passe à "terminee"

    Le tout dans une transaction atomique : si une étape échoue,
    rien n'est commité (pas de participation orpheline, pas de
    points perdus, pas de statut incohérent).
    """
    with transaction.atomic():

        # 1. Créer la participation
        participation = Participation.objects.create(
            sollicitation=sollicitation,
            statut=Participation.Statut.CONFIRMEE,
        )

        # 2. Ajouter 100 points au donneur
        donneur = sollicitation.donneur
        donneur.points_total += 100
        donneur.save(update_fields=['points_total'])

        # 3. Vérifier si la demande est satisfaite
        demande = sollicitation.demande

        # Compter toutes les participations confirmées sur cette demande
        # (peu importe le donneur, on veut le total)
        total_poches = Participation.objects.filter(
            sollicitation__demande=demande,
            statut=Participation.Statut.CONFIRMEE,
        ).count()

        # Si on atteint ou dépasse la quantité demandée, on termine la demande
        if total_poches >= demande.quantite:
            demande.statut = demande.Statut.TERMINEE
            demande.save(update_fields=['statut'])

        return participation