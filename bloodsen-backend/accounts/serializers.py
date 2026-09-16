from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Utilisateur, InscriptionEnAttente, ProfilDonneur


class InscriptionDonneurSerializer(serializers.Serializer):
    """
    Valide les données d'inscription d'un donneur.

    Ce serializer ne crée PAS d'Utilisateur : il crée une
    InscriptionEnAttente (voir la méthode create() en bas).
    """

    # Les champs attendus depuis le formulaire Vue
    email = serializers.EmailField()
    mot_de_passe = serializers.CharField(write_only=True)
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    telephone = serializers.CharField(max_length=20)
    groupe_sanguin = serializers.ChoiceField(choices=ProfilDonneur.GROUPES_SANGUINS)
    region = serializers.CharField(max_length=100)
    ville = serializers.CharField(max_length=100)
    quartier = serializers.CharField(max_length=100)

    def validate_email(self, value):
        """
        Méthode appelée automatiquement par DRF pour valider le champ email.
        On en profite pour vérifier qu'aucun compte ni inscription
        en attente n'existe déjà avec cet email.
        """
        if Utilisateur.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Cet email est déjà associé à un compte."
            )

        if InscriptionEnAttente.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Une inscription est déjà en attente de vérification pour cet email."
            )

        return value

    def validate_mot_de_passe(self, value):
        """
        Applique les règles de sécurité définies dans settings.py
        (AUTH_PASSWORD_VALIDATORS : longueur min, pas trop commun, etc.).
        """
        validate_password(value)
        return value

    def create(self, validated_data):
        """
        Appelée par serializer.save() dans la vue.

        validated_data contient tous les champs validés. On extrait
        le mot de passe et l'email pour les traiter spécialement, et
        tout le reste devient les données du futur profil.
        """
        mot_de_passe = validated_data.pop('mot_de_passe')
        email = validated_data.pop('email')

        # Ce qu'il reste (nom, prenom, telephone, groupe_sanguin, region,
        # ville, quartier) = les données du profil donneur.
        donnees_profil = validated_data

        return InscriptionEnAttente.objects.create(
            email=email,
            # make_password() hash immédiatement le mot de passe :
            # même en attente de vérification, il n'est jamais en clair.
            mot_de_passe_hash=make_password(mot_de_passe),
            role=Utilisateur.Role.DONNEUR,
            donnees_profil=donnees_profil,
        )


class InscriptionStructureSerializer(serializers.Serializer):
    """
    Même logique que pour le donneur, avec les champs propres
    à une structure de santé.
    """

    email = serializers.EmailField()
    mot_de_passe = serializers.CharField(write_only=True)
    nom_structure = serializers.CharField(max_length=200)
    adresse = serializers.CharField(max_length=255)
    region = serializers.CharField(max_length=100)
    ville = serializers.CharField(max_length=100)
    quartier = serializers.CharField(max_length=100)

    def validate_email(self, value):
        if Utilisateur.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Cet email est déjà associé à un compte."
            )

        if InscriptionEnAttente.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Une inscription est déjà en attente de vérification pour cet email."
            )

        return value

    def validate_mot_de_passe(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        mot_de_passe = validated_data.pop('mot_de_passe')
        email = validated_data.pop('email')
        donnees_profil = validated_data

        return InscriptionEnAttente.objects.create(
            email=email,
            mot_de_passe_hash=make_password(mot_de_passe),
            role=Utilisateur.Role.STRUCTURE,
            donnees_profil=donnees_profil,
        )


class VerificationTokenSerializer(serializers.Serializer):
    """
    Valide les données envoyées à l'Étape 5 lors de la vérification :
    la page /verification-email côté Vue envoie le token reçu dans l'URL.
    """

    token = serializers.CharField()


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Personnalise le token JWT délivré à la connexion.

    Par défaut, le token ne contient que l'id utilisateur. On y ajoute
    le "role" et l'email : pratique côté frontend pour rediriger
    directement vers /structure ou /donneur sans appel API supplémentaire.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # On ajoute nos champs personnalisés au payload du token.
        # Ces valeurs sont dans le token lui-même (décodable côté frontend
        # sans requête vers l'API).
        token['role'] = user.role
        token['email'] = user.email

        return token