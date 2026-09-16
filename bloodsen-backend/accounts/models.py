import secrets
from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UtilisateurManager


class Utilisateur(AbstractBaseUser, PermissionsMixin):

    # Les différents rôles possibles d'un utilisateur
    class Role(models.TextChoices):
        DONNEUR = 'donneur', 'Donneur'
        STRUCTURE = 'structure', 'Structure de santé'
        ADMIN = 'admin', 'Administrateur'

    # Adresse email unique de l'utilisateur
    email = models.EmailField(
        unique=True,
        verbose_name="Adresse email"
    )

    # Rôle de l'utilisateur
    role = models.CharField(
        max_length=20,
        choices=Role.choices
    )

    # Date de création du compte
    date_creation = models.DateTimeField(auto_now_add=True)

    # Indique si le compte est actif
    is_active = models.BooleanField(default=True)

    # Indique si l'utilisateur peut accéder à l'administration Django
    is_staff = models.BooleanField(default=False)

    # Utiliser notre manager personnalisé
    objects = UtilisateurManager()

    # L'email sera utilisé pour se connecter
    USERNAME_FIELD = 'email'

    # Aucun autre champ obligatoire lors de la création
    REQUIRED_FIELDS = []

    # Représentation de l'utilisateur
    def __str__(self):
        return self.email

class ProfilDonneur(models.Model):
    """
    Informations spécifiques à un Utilisateur ayant le rôle "donneur".
    Relation 1-vers-1 : chaque donneur a exactement un profil.
    """

    GROUPES_SANGUINS = [
        ('O+', 'O+'), ('O-', 'O-'),
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    # OneToOneField + related_name : permet d'écrire
    # utilisateur.profil_donneur pour accéder au profil depuis l'utilisateur
    utilisateur = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE, related_name='profil_donneur'
    )

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    groupe_sanguin = models.CharField(max_length=3, choices=GROUPES_SANGUINS)
    region = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    quartier = models.CharField(max_length=100)

    # Indique si le donneur peut recevoir des sollicitations en ce moment
    disponible = models.BooleanField(default=True)

    # Système de gamification (points accumulés à chaque don confirmé)
    points_total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class ProfilStructureSante(models.Model):
    """
    Informations spécifiques à un Utilisateur ayant le rôle "structure".
    """

    utilisateur = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE, related_name='profil_structure'
    )

    nom_structure = models.CharField(max_length=200)
    adresse = models.CharField(max_length=255)
    region = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    quartier = models.CharField(max_length=100)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom_structure


class InscriptionEnAttente(models.Model):
    """
    Stocke une demande d'inscription (donneur OU structure) tant que
    l'email n'a pas encore été vérifié.

    tant qu'une ligne existe ici, AUCUN Utilisateur/Profil
    n'a été créé en base. C'est seulement au moment où le lien de
    vérification est cliqué  que le vrai compte est créé,
    et cette ligne est alors supprimée.
    """

    email = models.EmailField(unique=True)

    # Le mot de passe est déjà hashé au moment où on l'enregistre ici
    # (jamais stocké en clair, même temporairement)
    mot_de_passe_hash = models.CharField(max_length=255)

    role = models.CharField(max_length=20, choices=Utilisateur.Role.choices)

    # Les champs de profil diffèrent selon le rôle (nom/prenom/... pour un
    # donneur, nom_structure/adresse/... pour une structure). Plutôt que
    # de dupliquer deux jeux de colonnes ici, on stocke tout en JSON :
    # on sait déjà, grâce à "role", comment interpréter ce JSON plus tard.
    donnees_profil = models.JSONField(default=dict)

    # Token unique inclus dans le lien envoyé par email
    # (ex: https://bloodsen.sn/verification-email?token=xxxx)
    token = models.CharField(max_length=64, unique=True, default=secrets.token_urlsafe)

    date_creation = models.DateTimeField(auto_now_add=True)
    expire_a = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Si expire_a n'est pas encore défini (première création),
        # on fixe l'expiration à 24h après la demande.
        if not self.expire_a:
            self.expire_a = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def est_expire(self):
        # Petite méthode utilitaire utilisée à l'Étape 5 pour vérifier
        # si le lien cliqué est encore valable
        return timezone.now() > self.expire_a

    def __str__(self):
        return f"Inscription en attente — {self.email}"