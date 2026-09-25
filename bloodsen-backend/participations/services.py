from django.db import transaction
from .models import Participation
from .utils import envoyer_email_confirmation_participation


def confirmer_participation(sollicitation):
    """
    Logique métier déclenchée quand une structure confirme
    qu'un donneur a effectivement donné son sang.

    Quatre choses se passent :
      1. On crée la Participation (statut "confirmee")
      2. On RECALCULE les points du donneur à partir de ses participations
      3. On vérifie si la demande est maintenant satisfaite
      4. On envoie un email de confirmation au donneur

    Le tout dans une transaction atomique : si une étape échoue,
    rien n'est commité.

    Barème : 100 points par don confirmé.
    """
    POINTS_PAR_DON = 100

    with transaction.atomic():

        # 1. Créer la participation
        participation = Participation.objects.create(
            sollicitation=sollicitation,
            statut=Participation.Statut.CONFIRMEE,
        )

        # 2. RECALCULER les points du donneur
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

    # 4. Envoyer l'email de confirmation (EN DEHORS de la transaction)
    #    Si l'email échoue, on ne veut PAS annuler la participation déjà créée.
    try:
        envoyer_email_confirmation_participation(participation)
    except Exception as e:
        # On log l'erreur mais on ne bloque pas
        print(f"Erreur lors de l'envoi de l'email de confirmation : {e}")

    return participation