from django.db import models


class Demande(models.Model):
    """
    Demande de sang créée par une structure de santé.
    Contient le besoin exprimé (groupe, quantité, urgence, message).
    Le lieu n'est PAS stocké ici : il est accessible via `demande.structure`.
    """

    class Urgence(models.TextChoices):
        VITALE = 'vitale', 'Urgence vitale'
        URGENT = 'urgent', 'Urgent'
        PROGRAMME = 'programme', 'Programmé'

    class Statut(models.TextChoices):
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

    # Relation vers la structure qui crée la demande.
    # "accounts.ProfilStructureSante" en chaîne = évite un import circulaire.
    structure = models.ForeignKey(
        'accounts.ProfilStructureSante',
        on_delete=models.CASCADE,
        related_name='demandes',
    )

    groupe_sanguin = models.CharField(max_length=3, choices=GroupeSanguin.choices)
    quantite = models.PositiveIntegerField(
        help_text="Nombre de poches de sang nécessaires"
    )
    urgence = models.CharField(max_length=20, choices=Urgence.choices)

    # Message libre affiché aux donneurs sollicités
    message = models.TextField(blank=True)

    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.EN_COURS,
    )

    date_creation = models.DateTimeField(auto_now_add=True)
    date_limite = models.DateTimeField(
        help_text="Date/heure après laquelle la demande n'est plus valable"
    )

    def __str__(self):
        return f"Demande {self.groupe_sanguin} x{self.quantite} — {self.structure.nom_structure}"


class Sollicitation(models.Model):
    """
    Sollicitation envoyée à un donneur précis pour une demande précise.

    Une sollicitation est créée automatiquement par le système de matching
    quand une demande est publiée. Le donneur peut ensuite l'accepter ou la refuser.
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
    date_reponse = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date à laquelle le donneur a répondu (accepté ou refusé)",
    )

    class Meta:
        # Contrainte : un même donneur ne peut être sollicité qu'une seule fois
        # pour une même demande.
        unique_together = ('demande', 'donneur')

    def __str__(self):
        return f"Sollicitation {self.donneur} → {self.demande}"