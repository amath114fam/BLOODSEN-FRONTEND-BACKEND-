from django.core.mail import send_mail
from django.conf import settings


def envoyer_email_contact(message_contact):
    """
    Envoie deux emails :
      1. Un email à l'administrateur (toi) avec le contenu du message
      2. Un accusé de réception à l'utilisateur qui a envoyé le message

    Args:
        message_contact: l'objet MessageContact créé en base
    """
    # ==========================================
    # 1. EMAIL À L'ADMINISTRATEUR
    # ==========================================
    sujet_admin = f"Contact BloodSen - {message_contact.sujet}"

    corps_admin = (
        f"Nouveau message reçu depuis le formulaire de contact BloodSen.\n\n"
        f"---\n"
        f"Nom complet : {message_contact.nom_complet}\n"
        f"Email : {message_contact.email}\n"
        f"Sujet : {message_contact.sujet}\n"
        f"Date : {message_contact.date_envoi.strftime('%d/%m/%Y à %H:%M')}\n"
        f"---\n\n"
        f"Message :\n"
        f"{message_contact.message}\n\n"
        f"---\n"
        f"Pour répondre à cet utilisateur, écrivez à : {message_contact.email}\n"
    )

    send_mail(
        subject=sujet_admin,
        message=corps_admin,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.CONTACT_EMAIL],
    )

    # ==========================================
    # 2. ACCUSÉ DE RÉCEPTION À L'UTILISATEUR
    # ==========================================
    sujet_user = "Nous avons bien reçu votre message - BloodSen"

    corps_user = (
        f"Bonjour {message_contact.nom_complet},\n\n"
        f"Nous avons bien reçu votre message et nous vous en remercions.\n\n"
        f"Notre équipe vous répondra dans les plus brefs délais à l'adresse : "
        f"{message_contact.email}.\n\n"
        f"Récapitulatif de votre message :\n"
        f"---\n"
        f"Sujet : {message_contact.sujet}\n"
        f"Message : {message_contact.message}\n"
        f"---\n\n"
        f"Merci de votre intérêt pour BloodSen.\n\n"
        f"L'équipe BloodSen"
    )

    send_mail(
        subject=sujet_user,
        message=corps_user,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[message_contact.email],
    )