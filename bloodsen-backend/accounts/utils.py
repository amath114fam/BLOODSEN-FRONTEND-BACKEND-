from django.core.mail import send_mail
from django.conf import settings


def envoyer_email_verification(email, token):
    """
    Envoie l'email contenant le lien de vérification.

    Le token est inclus dans l'URL sous forme de query string :
        http://localhost:5173/verification-email?token=xxx

    C'est cette page Vue qui, en se chargeant, appellera notre API
    (/api/auth/verifier-email/) en lui transmettant le token.
    """

    # Construction du lien complet vers la page Vue de vérification
    lien = f"{settings.FRONTEND_URL}/verification-email?token={token}"

    sujet = "Vérifiez votre adresse email — BloodSen"

    # Message simple et clair : pas de HTML, pour rester lisible
    # dans n'importe quel client mail
    message = (
        "Bonjour,\n\n"
        "Merci de vous être inscrit(e) sur BloodSen.\n\n"
        "Cliquez sur le lien ci-dessous pour vérifier votre adresse email "
        "et activer votre compte :\n"
        f"{lien}\n\n"
        "Ce lien expire dans 24 heures.\n\n"
        "Si vous n'êtes pas à l'origine de cette inscription, "
        "vous pouvez simplement ignorer cet email.\n\n"
        "L'équipe BloodSen"
    )

    # send_mail() est la fonction haut niveau de Django :
    # elle gère l'encodage, le sujet, le routing vers le backend
    # (Brevo SMTP dans notre cas) en un seul appel.
    send_mail(
        subject=sujet,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )