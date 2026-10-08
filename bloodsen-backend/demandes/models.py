from django.db import models


class Demande(models.Model):
    """
    Demande de sang créée par une structure, un proche connecté ou un public.
    """

    # ---- Énumérations ----

    class TypeCreateur(models.TextChoices):
        STRUCTURE = 'structure', 'Structure de santé'
        PROCHE = 'proche', 'Proche (utilisateur connecté)'
        PUBLIC = 'public', 'Personne sans compte'

    class Urgence(models.TextChoices):
        VITALE = 'vitale', 'Urgence vitale'
        URGENT = 'urgent', 'Urgent'
        PROGRAMME = 'programme', 'Programme'

    class StatutDemande(models.TextChoices):
        EN_VERIFICATION = 'en_verification', 'En vérification'
        EN_COURS = 'en_cours', 'En cours'
        TERMINEE = 'terminee', 'Terminée'
        EXPIREE = 'expiree', 'Expirée'
        ANNULEE = 'annulee', 'Annulée'

    class GroupeSanguin(models.TextChoices):
        O_POS = 'O+', 'O+'
        O_NEG = 'O-', 'O-'
        A_POS = 'A+', 'A+'
        A_NEG = 'A-', 'A-'
        B_POS = 'B+', 'B+'
        B_NEG = 'B-', 'B-'
        AB_POS = 'AB+', 'AB+'
        AB_NEG = 'AB-', 'AB-'

    # ---- Champs principaux ----

    # Qui a créé la demande : structure, proche connecté ou public
    type_createur = models.CharField(
        max_length=20,
        choices=TypeCreateur.choices,
        default=TypeCreateur.STRUCTURE,
    )

    # Utilisateur connecté (uniquement si PROCHE)
    utilisateur = models.ForeignKey(
        'accounts.Utilisateur',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='demandes_creees',
    )

    # Structure propriétaire (uniquement si STRUCTURE)
    structure = models.ForeignKey(
        'accounts.ProfilStructureSante',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='demandes',
    )

    # Ville de la demande (donne la région via ville.region)
    ville = models.ForeignKey(
        'accounts.Ville',
        on_delete=models.PROTECT,
        related_name='demandes',
    )

    # Groupe sanguin recherché
    groupe_sanguin = models.CharField(max_length=3, choices=GroupeSanguin.choices)

    # Nombre de poches demandées
    quantite = models.PositiveIntegerField()

    # Niveau d'urgence
    urgence = models.CharField(max_length=20, choices=Urgence.choices)

    # Message libre affiché aux donneurs
    message = models.TextField(blank=True)

    # Statut courant de la demande
    statut = models.CharField(
        max_length=20,
        choices=StatutDemande.choices,
        default=StatutDemande.EN_COURS,
    )

    date_creation = models.DateTimeField(auto_now_add=True)
    date_limite = models.DateTimeField()

    # ---- Champs spécifiques aux demandes PROCHE / PUBLIC ----

    # Nom de la personne qui fait la demande (sans compte)
    nom_demandeur = models.CharField(max_length=200, blank=True)

    # Téléphone du demandeur (obligatoire pour PUBLIC)
    telephone_demandeur = models.CharField(max_length=20, blank=True)

    email_demandeur = models.EmailField(blank=True)

    # True quand le téléphone est validé par code SMS
    telephone_verifie = models.BooleanField(default=False)

    # Nom du patient concerné
    nom_patient = models.CharField(max_length=200, blank=True)

    # Hôpital où se trouve le patient
    lieu_prise_en_charge = models.CharField(max_length=255, blank=True)

    # Token pour suivre la demande sans compte
    token_suivi = models.CharField(max_length=64, unique=True, null=True, blank=True)

    # Coordonnées GPS de l'urgence (si PUBLIC)
    latitude_urgence = models.FloatField(null=True, blank=True)
    longitude_urgence = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Demande {self.groupe_sanguin} x{self.quantite} - {self.ville}"


class Sollicitation(models.Model):
    """
    Sollicitation envoyée à un donneur pour une demande.
    """

    class Statut(models.TextChoices):
        EN_ATTENTE = 'en_attente', 'En attente'
        ACCEPTEE = 'acceptee', 'Acceptée'
        REFUSEE = 'refusee', 'Refusée'
        EXPIREE = 'expiree', 'Expirée'

    demande = models.ForeignKey(
        Demande,
        on_delete=models.CASCADE,
        related_name='sollicitations',
    )
    donneur = models.ForeignKey(
        'accounts.ProfilDonneur',
        on_delete=models.CASCADE,
        related_name='sollicitations',
    )

    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.EN_ATTENTE,
    )

    date_creation = models.DateTimeField(auto_now_add=True)
    date_reponse = models.DateTimeField(null=True, blank=True)

    # Distance entre la demande et le donneur (calculée au moment du matching)
    distance_km = models.FloatField(null=True, blank=True)

    class Meta:
        # Un donneur ne peut être sollicité qu'une fois par demande
        unique_together = ('demande', 'donneur')

    def __str__(self):
        return f"Sollicitation {self.donneur} - {self.demande}"