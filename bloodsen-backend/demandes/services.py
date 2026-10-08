from datetime import timedelta

from django.db.models import Max, Q
from django.utils import timezone

from accounts.models import ProfilDonneur
from .models import Sollicitation
from .utils import envoyer_email_sollicitation


def trouver_donneurs_compatibles(demande):
    """
    Retourne les donneurs compatibles avec une demande.
    Fonctionne pour les 3 types : STRUCTURE, PROCHE, PUBLIC.

    Critères :
      - même groupe sanguin
      - même région (via demande.ville.region)
      - disponible == True
      - dernier don > 7 jours (ou jamais donné)
    """
    seuil = timezone.now() - timedelta(days=7)

    # La région vient toujours de demande.ville
    region = demande.ville.region

    donneurs = (
        ProfilDonneur.objects
        .filter(
            groupe_sanguin=demande.groupe_sanguin,
            ville__region=region,
            disponible=True,
        )
        .annotate(
            dernier_don=Max('sollicitations__participation__date_confirmation')
        )
        .filter(
            Q(dernier_don__isnull=True) | Q(dernier_don__lt=seuil)
        )
    )
    return list(donneurs)


def creer_sollicitations_pour_demande(demande):
    """
    Crée les sollicitations pour une demande donnée.

    Retourne la liste des Sollicitation nouvellement créées.
    """
    donneurs = trouver_donneurs_compatibles(demande)

    sollicitations = []
    for donneur in donneurs:
        sollicitation = Sollicitation.objects.create(
            demande=demande,
            donneur=donneur,
            statut=Sollicitation.Statut.EN_ATTENTE,
        )

        envoyer_email_sollicitation(sollicitation)
         
        sollicitations.append(sollicitation)

    return sollicitations

