import logging

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


def envoyer_email_contact(message_contact):
    """
    Envoie deux emails :
      1. Un email à l'équipe BloodSen avec le message reçu
      2. Un accusé de réception à la personne qui a écrit

    Retourne True si les deux envois ont réussi, False sinon.

    Args:
        message_contact: l'objet MessageContact créé en base
    """
    date = message_contact.date_envoi.strftime("%d/%m/%Y")
    heure = message_contact.date_envoi.strftime("%H:%M")

    succes = True

    # ==========================================
    # 1. EMAIL À L'ÉQUIPE
    # ==========================================
    sujet_admin = f"Nouveau message de {message_contact.nom_complet} : {message_contact.sujet}"

    corps_admin = (
        f"Bonjour,\n\n"
        f"{message_contact.nom_complet} ({message_contact.email}) vous a écrit "
        f"le {date} à {heure} depuis le formulaire de contact de BloodSen, "
        f"à propos de « {message_contact.sujet} ».\n\n"
        f"Voici son message :\n\n"
        f"{message_contact.message}\n\n"
        f"Vous pouvez lui répondre directement en répondant à cet email.\n\n"
        f"Cordialement,\n"
        f"BloodSen"
    )

    try:
        EmailMessage(
            subject=sujet_admin,
            body=corps_admin,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_EMAIL],
            reply_to=[message_contact.email],
        ).send()
    except Exception:
        logger.exception("Échec de l'envoi de l'email à l'équipe")
        succes = False

    # ==========================================
    # 2. ACCUSÉ DE RÉCEPTION À L'UTILISATEUR
    # ==========================================
    sujet_user = "Nous avons bien reçu votre message"

    corps_user = (
        f"Bonjour {message_contact.nom_complet},\n\n"
        f"Merci de nous avoir contactés. Nous avons bien reçu votre message "
        f"concernant « {message_contact.sujet} » et notre équipe vous répondra "
        f"dans les meilleurs délais.\n\n"
        f"Pour rappel, voici ce que vous nous avez écrit :\n\n"
        f"{message_contact.message}\n\n"
        f"Cordialement,\n"
        f"L'équipe BloodSen"
    )

    try:
        EmailMessage(
            subject=sujet_user,
            body=corps_user,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[message_contact.email],
        ).send()
    except Exception:
        logger.exception("Échec de l'envoi de l'accusé de réception")
        succes = False

    return succes