from datetime import timedelta
from math import radians, sin, cos, asin, sqrt
from django.db.models import Max, Q
from django.utils import timezone

from accounts.models import ProfilDonneur
from .models import Sollicitation
from .utils import envoyer_email_sollicitation


# Nombre maximum de donneurs sollicités par demande
MAX_DONNEURS_PAR_DEMANDE = 20

# Délai minimum entre deux dons (en jours)
DELAI_MIN_ENTRE_DONS = 7


def calculer_distance_km(lat1, lon1, lat2, lon2):
    """
    Calcule la distance entre deux points GPS avec la formule de Haversine.
    Renvoie la distance en kilomètres.
    """
    # Rayon de la Terre en km
    R = 6371.0

    # Conversion en radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # La formule de Haversine
    # a = sin²(Δφ/2) + cos(φ1) × cos(φ2) × sin²(Δλ/2)

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * R * asin(sqrt(a))


def _coordonnees_demande(demande):
    """
    Renvoie les coordonnées GPS de la demande selon son type.
    - STRUCTURE : coordonnées de la structure
    - PROCHE / PUBLIC : coordonnées saisies dans la demande
    """
    if demande.structure and demande.structure.latitude and demande.structure.longitude:
        return (demande.structure.latitude, demande.structure.longitude)
    if demande.latitude_urgence and demande.longitude_urgence:
        return (demande.latitude_urgence, demande.longitude_urgence)
    return None


# =====================================================
# CONSTANTES
# =====================================================

MAX_DONNEURS_PAR_DEMANDE = 20
DELAI_MIN_ENTRE_DONS = 7
RAYON_MAX_KM = 50


def trouver_donneurs_compatibles(demande):
    """
    Retourne les donneurs compatibles avec une demande, en cascade :

    Niveau 1 : donneurs AVEC coordonnées dans RAYON_MAX_KM, triés par distance.
    Niveau 2 : donneurs SANS coordonnées, de la même ville.
    Niveau 3 : donneurs SANS coordonnées, de la même région.

    On remplit la liste niveau par niveau jusqu'à MAX_DONNEURS_PAR_DEMANDE.

    Renvoie une liste de tuples (donneur, distance_km).
    distance_km vaut None pour les niveaux 2 et 3.
    """
    seuil = timezone.now() - timedelta(days=DELAI_MIN_ENTRE_DONS)
    region = demande.ville.region
    ville = demande.ville

    # Base commune : tous les donneurs compatibles (sans filtre géo)
    base = (
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

    # Coordonnées de la demande (peuvent être absentes)
    coords = _coordonnees_demande(demande)

    resultats = []       # liste finale (donneur, distance)
    deja_ajoutes = set()  # ids des donneurs déjà ajoutés

    # ==========================================
    # Niveau 1 : AVEC coordonnées, dans le rayon
    # ==========================================
    if coords:
        lat_d, lon_d = coords
        niveau1 = []

        for donneur in base.exclude(latitude__isnull=True).exclude(longitude__isnull=True):
            distance = calculer_distance_km(
                lat_d, lon_d, donneur.latitude, donneur.longitude
            )
            if distance <= RAYON_MAX_KM:
                niveau1.append((donneur, distance))

        # Tri par distance croissante
        niveau1.sort(key=lambda x: x[1])

        for donneur, distance in niveau1:
            if len(resultats) >= MAX_DONNEURS_PAR_DEMANDE:
                break
            resultats.append((donneur, distance))
            deja_ajoutes.add(donneur.id)

    # Si on a déjà N donneurs, on s'arrête
    if len(resultats) >= MAX_DONNEURS_PAR_DEMANDE:
        return resultats

        # ==========================================
    # Niveau 2 : même ville
    # (avec ou sans coordonnées, peu importe si la demande n'a pas de GPS)
    # ==========================================
    niveau2 = (
        base
        .filter(ville=ville)
        .exclude(id__in=deja_ajoutes)
    )

    for donneur in niveau2:
        if len(resultats) >= MAX_DONNEURS_PAR_DEMANDE:
            break
        resultats.append((donneur, None))
        deja_ajoutes.add(donneur.id)

    if len(resultats) >= MAX_DONNEURS_PAR_DEMANDE:
        return resultats

    # ==========================================
    # Niveau 3 : même région
    # ==========================================
    niveau3 = (
        base
        .exclude(ville=ville)
        .exclude(id__in=deja_ajoutes)
    )

    for donneur in niveau3:
        if len(resultats) >= MAX_DONNEURS_PAR_DEMANDE:
            break
        resultats.append((donneur, None))

    return resultats

def creer_sollicitations_pour_demande(demande):
    """
    Crée les sollicitations pour les donneurs compatibles.
    Enregistre aussi la distance dans chaque Sollicitation.
    """
    resultats = trouver_donneurs_compatibles(demande)
    sollicitations = []

    for donneur, distance in resultats:
        sollicitation = Sollicitation.objects.create(
            demande=demande,
            donneur=donneur,
            statut=Sollicitation.Statut.EN_ATTENTE,
            distance_km=distance,
        )
        envoyer_email_sollicitation(sollicitation)
        sollicitations.append(sollicitation)

    return sollicitations