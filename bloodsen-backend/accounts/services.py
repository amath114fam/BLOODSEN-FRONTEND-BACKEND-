from datetime import timedelta
from django.utils import timezone
from .models import Niveau, Badge, BadgeObtenu, ProfilDonneur


# =====================================================
# ATTRIBUTION AUTOMATIQUE DES NIVEAUX ET BADGES
# =====================================================

def mettre_a_jour_niveau(donneur):
    """
    Met à jour le niveau du donneur selon son points_total.
    Renvoie True si le niveau a changé.
    """
    nouveau_niveau = (
        Niveau.objects
        .filter(points_requis__lte=donneur.points_total)
        .order_by('-points_requis')
        .first()
    )

    if nouveau_niveau and donneur.niveau != nouveau_niveau:
        donneur.niveau = nouveau_niveau
        donneur.save(update_fields=['niveau'])
        return True

    return False


def _condition_badge_remplie(donneur, badge):
    """
    Vérifie si la condition d'un badge est remplie pour un donneur.
    Renvoie True/False.
    """
    nom = badge.nom

    # Compter les dons confirmés
    nb_dons = donneur.sollicitations.filter(
        participation__statut='confirmee',
    ).count()

    if nom == 'Premier don':
        return nb_dons >= 1

    if nom == 'Donneur régulier':
        return nb_dons >= 5

    if nom == 'Donneur engagé':
        return nb_dons >= 10

    if nom == 'Sauveur d\'urgence':
        return donneur.sollicitations.filter(
            participation__statut='confirmee',
            demande__urgence='vitale',
        ).exists()

    if nom == 'Fidèle':
        return (timezone.now() - donneur.utilisateur.date_creation) >= timedelta(days=365)

    if nom == 'Profil complet':
        return bool(
            donneur.telephone
            and donneur.ville
            and donneur.latitude
            and donneur.longitude
        )

    return False


def attribuer_badges(donneur):
    """
    Attribue automatiquement les badges dont la condition est remplie.
    Renvoie la liste des badges nouvellement obtenus.
    """
    badges_obtenus_ids = set(
        BadgeObtenu.objects.filter(donneur=donneur).values_list('badge_id', flat=True)
    )

    nouveaux = []
    for badge in Badge.objects.exclude(id__in=badges_obtenus_ids):
        if _condition_badge_remplie(donneur, badge):
            BadgeObtenu.objects.create(donneur=donneur, badge=badge)
            nouveaux.append(badge)

    return nouveaux


def verifier_gamification(donneur):
    """
    Fonction appelée après chaque don confirmé.
    Met à jour le niveau et attribue les badges.

    Renvoie un dict avec le résultat.
    """
    niveau_change = mettre_a_jour_niveau(donneur)
    nouveaux_badges = attribuer_badges(donneur)

    return {
        'niveau_change': niveau_change,
        'nouveau_niveau': donneur.niveau,
        'nouveaux_badges': [b.nom for b in nouveaux_badges],
    }