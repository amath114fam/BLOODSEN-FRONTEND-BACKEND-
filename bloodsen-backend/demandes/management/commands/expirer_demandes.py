from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction

from demandes.models import Demande, Sollicitation


def executer_expiration_demandes():
    """
    Logique métier de l'expiration des demandes.

    Peut être appelée :
      - depuis la commande Django (cron, manuel)
      - depuis une vue (dashboard, suivi de demande)

    Renvoie un dict avec le nombre de demandes et sollicitations expirées.
    """
    maintenant = timezone.now()

    # 1. Trouver les demandes à expirer
    demandes_a_expirer = Demande.objects.filter(
        statut=Demande.StatutDemande.EN_COURS,
        date_limite__lt=maintenant,
    )

    nb_demandes = demandes_a_expirer.count()

    if nb_demandes == 0:
        return {
            "demandes": 0,
            "sollicitations": 0,
        }

    # 2. Transaction atomique
    with transaction.atomic():
        nb_sollicitations = Sollicitation.objects.filter(
            demande__in=demandes_a_expirer,
            statut=Sollicitation.Statut.EN_ATTENTE,
        ).update(statut=Sollicitation.Statut.EXPIREE)

        demandes_a_expirer.update(statut=Demande.StatutDemande.EXPIREE)

    return {
        "demandes": nb_demandes,
        "sollicitations": nb_sollicitations,
    }


class Command(BaseCommand):
    """
    Expire les demandes dont la date_limite est dépassée.

    Utilisation :
        python manage.py expirer_demandes
    """

    help = "Expire les demandes dont la date limite est dépassée."

    def handle(self, *args, **options):
        resultat = executer_expiration_demandes()

        if resultat["demandes"] == 0:
            self.stdout.write(
                self.style.SUCCESS("Aucune demande à expirer.")
            )
            return

        self.stdout.write(self.style.SUCCESS(
            f"{resultat['demandes']} demande(s) expirée(s), "
            f"{resultat['sollicitations']} sollicitation(s) en attente expirée(s)."
        ))