from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .constants import (
    REGIONS_CHOICES,
    normaliser_telephone,
    valider_nom_propre,
)

from .models import Utilisateur, InscriptionEnAttente, ProfilDonneur


class InscriptionDonneurSerializer(serializers.Serializer):
    """
    Valide les données d'inscription d'un donneur.

    Ce serializer ne crée PAS d'Utilisateur : il crée une
    InscriptionEnAttente (voir la méthode create() en bas).
    """

    # Les champs attendus depuis le formulaire Vue
    email = serializers.EmailField()
    mot_de_passe = serializers.CharField(write_only=True, max_length=128)
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    telephone = serializers.CharField(max_length=20)
    groupe_sanguin = serializers.ChoiceField(choices=ProfilDonneur.GROUPES_SANGUINS)
    region = serializers.ChoiceField(choices=REGIONS_CHOICES)
    ville = serializers.CharField(max_length=100)
    quartier = serializers.CharField(max_length=100)

    def validate_email(self, value):
        """
        Vérifie que l'email n'est pas déjà utilisé.
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
        Applique les règles de sécurité de Django.
        """
        validate_password(value)
        return value

    def validate_nom(self, value):
        """
        Valide le nom (lettres, longueur minimale).
        """
        try:
            return valider_nom_propre(value, 'le nom', min_length=2)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def validate_prenom(self, value):
        """
        Valide le prénom (lettres, longueur minimale).
        """
        try:
            return valider_nom_propre(value, 'le prénom', min_length=2)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def validate_telephone(self, value):
        """
        Normalise et valide le téléphone sénégalais.
        """
        try:
            return normaliser_telephone(value)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def validate_ville(self, value):
        """
        Valide la ville (longueur minimale).
        """
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "La ville doit contenir au moins 2 caractères."
            )
        return value.strip()

    def validate_quartier(self, value):
        """
        Valide le quartier (longueur minimale).
        """
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Le quartier doit contenir au moins 2 caractères."
            )
        return value.strip()

    def create(self, validated_data):
        """
        Crée une InscriptionEnAttente (PAS un Utilisateur).
        """
        mot_de_passe = validated_data.pop('mot_de_passe')
        email = validated_data.pop('email')

        donnees_profil = validated_data

        return InscriptionEnAttente.objects.create(
            email=email,
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
    mot_de_passe = serializers.CharField(write_only=True, max_length=128)
    nom_structure = serializers.CharField(max_length=200)
    adresse = serializers.CharField(max_length=255)
    region = serializers.ChoiceField(choices=REGIONS_CHOICES)
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

    def validate_nom_structure(self, value):
        """
        Valide le nom de la structure (lettres, longueur minimale 3).
        """
        try:
            return valider_nom_propre(value, 'le nom de la structure', min_length=3, max_length=200)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def validate_adresse(self, value):
        """
        Valide l'adresse (longueur minimale 5).
        """
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                "L'adresse doit contenir au moins 5 caractères."
            )
        return value.strip()

    def validate_ville(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "La ville doit contenir au moins 2 caractères."
            )
        return value.strip()

    def validate_quartier(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Le quartier doit contenir au moins 2 caractères."
            )
        return value.strip()

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