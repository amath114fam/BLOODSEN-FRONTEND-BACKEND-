from django.db import models


class MessageContact(models.Model):
    """
    Message envoyé depuis le formulaire de contact de la page d'accueil.
    """
    nom_complet = models.CharField(max_length=200)
    email = models.EmailField()
    sujet = models.CharField(max_length=255)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(
        default=False,
        help_text="True si le message a été traité",
    )

    class Meta:
        ordering = ['-date_envoi']

    def __str__(self):
        return f"{self.sujet} - {self.email}"