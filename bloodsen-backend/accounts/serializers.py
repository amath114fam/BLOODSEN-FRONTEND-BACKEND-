from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .constants import (
    REGIONS_CHOICES,
    normaliser_telephone,
    valider_nom_propre,
)

from .models import Utilisateur, InscriptionEnAttente, ProfilDonneur, TokenReinitialisationMotDePasse


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


# =====================================================
# SERIALIZER : modification du profil donneur
# =====================================================

class ModifierProfilDonneurSerializer(serializers.Serializer):
    """
    Valide les données de modification du profil d'un donneur.
    Seuls certains champs sont modifiables :
      - nom, prenom
      - telephone
      - region, ville, quartier
      - disponible

    Le groupe sanguin et l'email ne sont PAS modifiables.
    """
    nom = serializers.CharField(max_length=100, required=False)
    prenom = serializers.CharField(max_length=100, required=False)
    telephone = serializers.CharField(max_length=20, required=False)
    region = serializers.ChoiceField(choices=REGIONS_CHOICES, required=False)
    ville = serializers.CharField(max_length=100, required=False)
    quartier = serializers.CharField(max_length=100, required=False)
    disponible = serializers.BooleanField(required=False)

    def validate_nom(self, value):
        try:
            return valider_nom_propre(value, 'le nom', min_length=2)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def validate_prenom(self, value):
        try:
            return valider_nom_propre(value, 'le prénom', min_length=2)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def validate_telephone(self, value):
        try:
            return normaliser_telephone(value)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

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

    def update(self, instance, validated_data):
        """
        Met à jour le ProfilDonneur avec les données validées.
        Seuls les champs fournis sont modifiés.
        """
        for champ, valeur in validated_data.items():
            setattr(instance, champ, valeur)
        instance.save()
        return instance


# =====================================================
# SERIALIZER : modification du profil structure
# =====================================================

class ModifierProfilStructureSerializer(serializers.Serializer):
    """
    Valide les données de modification du profil d'une structure.
    Champs modifiables :
      - nom_structure
      - adresse
      - region, ville, quartier

    L'email ne est PAS modifiable.
    """
    nom_structure = serializers.CharField(max_length=200, required=False)
    adresse = serializers.CharField(max_length=255, required=False)
    region = serializers.ChoiceField(choices=REGIONS_CHOICES, required=False)
    ville = serializers.CharField(max_length=100, required=False)
    quartier = serializers.CharField(max_length=100, required=False)

    def validate_nom_structure(self, value):
        try:
            return valider_nom_propre(
                value, 'le nom de la structure',
                min_length=3, max_length=200,
            )
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def validate_adresse(self, value):
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

    def update(self, instance, validated_data):
        for champ, valeur in validated_data.items():
            setattr(instance, champ, valeur)
        instance.save()
        return instance


# =====================================================
# SERIALIZER : changement de mot de passe
# =====================================================

class ChangerMotDePasseSerializer(serializers.Serializer):
    """
    Valide les données de changement de mot de passe.

    Champs attendus :
      - mot_de_passe_actuel : pour vérifier que c'est bien l'utilisateur
      - nouveau_mot_de_passe : le nouveau (validé par les règles Django)
    """
    mot_de_passe_actuel = serializers.CharField(write_only=True)
    nouveau_mot_de_passe = serializers.CharField(write_only=True, max_length=128)

    def validate_mot_de_passe_actuel(self, value):
        """
        Vérifie que le mot de passe actuel est correct.
        On accède à l'utilisateur via self.context['request'].user.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                "Le mot de passe actuel est incorrect."
            )
        return value

    def validate_nouveau_mot_de_passe(self, value):
        """
        Applique les règles de sécurité Django au nouveau mot de passe.
        """
        validate_password(value)
        return value

    def validate(self, data):
        """
        Vérification globale : le nouveau doit être différent de l'actuel.
        """
        if data['mot_de_passe_actuel'] == data['nouveau_mot_de_passe']:
            raise serializers.ValidationError(
                {"nouveau_mot_de_passe": "Le nouveau mot de passe doit être différent de l'ancien."}
            )
        return data

    def save(self, **kwargs):
        """
        Enregistre le nouveau mot de passe sur l'utilisateur.
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['nouveau_mot_de_passe'])
        user.save()
        return user

# =====================================================
# SERIALIZERS : mot de passe oublié
# =====================================================

class MotDePasseOublieSerializer(serializers.Serializer):
    """
    Valide l'email saisi pour la demande de réinitialisation.
    On NE vérifie PAS si l'email existe (sécurité : éviter l'énumération).
    """
    email = serializers.EmailField()


class ReinitialiserMotDePasseSerializer(serializers.Serializer):
    """
    Valide le token et le nouveau mot de passe.
    """
    token = serializers.CharField()
    nouveau_mot_de_passe = serializers.CharField(write_only=True, max_length=128)

    def validate_nouveau_mot_de_passe(self, value):
        validate_password(value)
        return value

    def validate_token(self, value):
        """
        Vérifie que le token existe, n'a pas expiré et n'a pas été utilisé.
        """
        try:
            token_obj = TokenReinitialisationMotDePasse.objects.get(token=value)
        except TokenReinitialisationMotDePasse.DoesNotExist:
            raise serializers.ValidationError(
                "Ce lien de réinitialisation est invalide."
            )

        if not token_obj.est_valide():
            raise serializers.ValidationError(
                "Ce lien de réinitialisation a expiré ou a déjà été utilisé."
            )

        # On stocke l'objet token dans le serializer pour le réutiliser dans save()
        self._token_obj = token_obj
        return value

    def save(self, **kwargs):
        """
        Change le mot de passe et marque le token comme utilisé.
        """
        token_obj = self._token_obj
        utilisateur = token_obj.utilisateur

        utilisateur.set_password(self.validated_data['nouveau_mot_de_passe'])
        utilisateur.save()

        token_obj.utilise = True
        token_obj.save(update_fields=['utilise'])

        return utilisateur