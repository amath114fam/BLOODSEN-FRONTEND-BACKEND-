from django.db import models


class Participation(models.Model):
    """
    Participation effective d'un donneur à une demande de sang.

    Créée uniquement quand la structure CONFIRME que le donneur s'est
    présenté au centre de collecte. Un donneur peut avoir accepté une
    sollicitation sans pour autant venir faire le don : c'est justement
    la confirmation par la structure qui crée la Participation.
    
    """

    class Statut(models.TextChoices):
        CONFIRMEE = 'confirmee', 'Confirmée'
        ANNULEE = 'annulee', 'Annulée'

    # OneToOneField : garantit au niveau base de données qu'il ne peut y avoir
    # qu'UNE seule participation par sollicitation.
    sollicitation = models.OneToOneField(
        'demandes.Sollicitation',
        on_delete=models.CASCADE,
        related_name='participation',
    )

    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.CONFIRMEE,
    )

    # Date à laquelle la structure a confirmé la participation
    date_confirmation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Participation {self.sollicitation.donneur} — {self.statut}"