from django.contrib.auth.base_user import BaseUserManager


class UtilisateurManager(BaseUserManager):
    """
    Manager personnalisé pour créer les utilisateurs.
    """

    def create_user(self, email, password=None, **extra_fields):
        # Vérifier que l'utilisateur a fourni un email
        if not email:
            raise ValueError("L'adresse email est obligatoire.")

        # Normaliser l'email pour éviter certaines différences de casse
        email = self.normalize_email(email)

        # Préparer le nouvel utilisateur avec ses informations
        utilisateur = self.model(
            email=email,
            **extra_fields
        )

        # Hacher le mot de passe avant de l'enregistrer
        utilisateur.set_password(password)

        # Enregistrer l'utilisateur dans la base de données
        utilisateur.save(using=self._db)

        # Retourner l'utilisateur créé
        return utilisateur

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Créer un superutilisateur pour l'administration Django.
        """

        # Autoriser l'accès à l'interface d'administration
        extra_fields.setdefault('is_staff', True)

        # Donner tous les droits d'administration
        extra_fields.setdefault('is_superuser', True)

        # Définir un rôle par défaut pour le superutilisateur
        extra_fields.setdefault('role', 'admin')

        # Réutiliser create_user pour créer le compte
        return self.create_user(
            email,
            password,
            **extra_fields
        )