from datetime import timedelta

from django.db.models import Max, Q
from django.utils import timezone

from accounts.models import ProfilDonneur
from .models import Sollicitation
from .utils import envoyer_email_sollicitation


def trouver_donneurs_compatibles(demande):
    """
    Retourne la liste des ProfilDonneur compatibles avec une demande.

    Critères de matching (V1) :
    - même groupe sanguin que la demande
    - même région que la structure
    - même ville que la structure
    - disponible == True
    - dernier don > 7 jours (ou jamais donné)
    """
    seuil = timezone.now() - timedelta(days=7)

    # On part de tous les donneurs et on applique les filtres.
    # La jointure "sollicitations__participation__date_confirmation"
    # traverse la chaîne de relations pour atteindre la date du dernier don.
    donneurs = (
        ProfilDonneur.objects
        .filter(
            groupe_sanguin=demande.groupe_sanguin,
            region=demande.structure.region,
            ville=demande.structure.ville,
            disponible=True,
        )
        .annotate(
            # Max() ajoute un champ calculé "dernier_don" à chaque donneur
            dernier_don=Max('sollicitations__participation__date_confirmation')
        )
        .filter(
            # On garde les donneurs qui n'ont JAMAIS donné (dernier_don = None)
            # OU dont le dernier don est antérieur au seuil de 7 jours.
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

