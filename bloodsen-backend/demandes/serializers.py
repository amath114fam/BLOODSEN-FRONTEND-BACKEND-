from rest_framework import serializers

from .models import Demande, Sollicitation
from participations.models import Participation

from django.utils import timezone
from datetime import timedelta
from accounts.models import Ville
import secrets
from accounts.constants import normaliser_telephone


class DemandeCreateSerializer(serializers.ModelSerializer):
    """
    Serializer utilisé pour CRÉER une demande (POST).
    On n'expose que les champs que la structure doit fournir.
    La structure est déduite de l'utilisateur connecté : pas besoin
    de la passer dans le payload.
    """
    class Meta:
        model = Demande
        fields = [
            'id',
            'groupe_sanguin',
            'quantite',
            'urgence',
            'message',
            'date_limite',
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'groupe_sanguin': {
                'error_messages': {
                    'required': "Veuillez choisir un groupe sanguin.",
                    'null': "Veuillez choisir un groupe sanguin.",
                    'invalid_choice': "Veuillez choisir un groupe sanguin valide.",
                },
            },
        }

    def validate_groupe_sanguin(self, value):
        """
        Vérifie que le groupe sanguin est dans la liste autorisée.
        (ChoiceField sur le modèle, mais on rend l'erreur explicite.)
        """
        groupes_valides = [g[0] for g in Demande.GroupeSanguin.choices]
        if value not in groupes_valides:
            raise serializers.ValidationError(
                f"Groupe sanguin invalide. Valeurs autorisées : {', '.join(groupes_valides)}."
            )
        return value

    def validate_urgence(self, value):
        """
        Vérifie que le niveau d'urgence est valide.
        """
        urgences_valides = [u[0] for u in Demande.Urgence.choices]
        if value not in urgences_valides:
            raise serializers.ValidationError(
                f"Niveau d'urgence invalide. Valeurs autorisées : {', '.join(urgences_valides)}."
            )
        return value

    def validate_quantite(self, value):
        """
        La quantité doit être au minimum 1 poche.
        Pas de maximum (une structure peut avoir besoin de beaucoup de poches).
        """
        if value < 1:
            raise serializers.ValidationError(
                "La quantité doit être d'au moins 1 poche."
            )
        return value

    def validate_message(self, value):
        """
        Le message ne doit pas dépasser 1000 caractères.
        """
        if value and len(value) > 1000:
            raise serializers.ValidationError(
                "Le message ne peut pas dépasser 1000 caractères."
            )
        return value

    def validate_date_limite(self, value):
        """
        La date limite doit :
          - être dans le futur (au moins 1 heure après maintenant)
          - ne pas être trop loin dans le futur (max 30 jours)
        """
        maintenant = timezone.now()
        marge_minimum = maintenant + timedelta(hours=1)
        marge_maximum = maintenant + timedelta(days=30)

        if value < marge_minimum:
            raise serializers.ValidationError(
                "La date limite doit être au moins 1 heure dans le futur."
            )

        if value > marge_maximum:
            raise serializers.ValidationError(
                "La date limite ne peut pas dépasser 30 jours dans le futur."
            )

        return value


class DemandeSerializer(serializers.ModelSerializer):
    """
    Lecture d'une demande (STRUCTURE, PROCHE ou PUBLIC).
    """
    # Nom + localisation selon le type
    structure_nom = serializers.SerializerMethodField()
    structure_region = serializers.SerializerMethodField()
    structure_ville = serializers.SerializerMethodField()

    nombre_sollicitations = serializers.IntegerField(
        source='sollicitations.count',
        read_only=True,
    )
    nombre_sollicitations_en_attente = serializers.SerializerMethodField()
    nombre_participations_confirmees = serializers.SerializerMethodField()

    class Meta:
        model = Demande
        fields = [
            'id',
            'type_createur',
            'structure_nom',
            'structure_region',
            'structure_ville',
            'groupe_sanguin',
            'quantite',
            'urgence',
            'message',
            'statut',
            'date_creation',
            'date_limite',
            'nombre_sollicitations',
            'nombre_sollicitations_en_attente',
            'nombre_participations_confirmees',
        ]

    def get_structure_nom(self, obj):
        # STRUCTURE : nom_structure ; PROCHE/PUBLIC : lieu saisi
        if obj.structure:
            return obj.structure.nom_structure
        return obj.lieu_prise_en_charge or "—"

    def get_structure_region(self, obj):
        # La région vient toujours de demande.ville
        return obj.ville.region.nom if obj.ville else "—"

    def get_structure_ville(self, obj):
        return obj.ville.nom if obj.ville else "—"

    def get_nombre_sollicitations_en_attente(self, obj):
        return obj.sollicitations.filter(statut='en_attente').count()

    def get_nombre_participations_confirmees(self, obj):
        return Participation.objects.filter(
            sollicitation__demande=obj,
            statut='confirmee',
        ).count()


    
class SollicitationSerializer(serializers.ModelSerializer):
    """
    Lecture d'une sollicitation, adaptée aux 3 types de demandes.
    """
    demande_id = serializers.IntegerField(source='demande.id', read_only=True)

    structure_nom = serializers.SerializerMethodField()
    structure_region = serializers.SerializerMethodField()
    structure_ville = serializers.SerializerMethodField()

    groupe_sanguin = serializers.CharField(source='demande.groupe_sanguin', read_only=True)
    urgence = serializers.CharField(source='demande.urgence', read_only=True)
    message = serializers.CharField(source='demande.message', read_only=True)

    class Meta:
        model = Sollicitation
        fields = [
            'id',
            'demande_id',
            'structure_nom',
            'structure_region',
            'structure_ville',
            'groupe_sanguin',
            'urgence',
            'message',
            'statut',
            'date_creation',
            'date_reponse',
            'distance_km',
        ]

    def get_structure_nom(self, obj):
        if obj.demande.structure:
            return obj.demande.structure.nom_structure
        return obj.demande.lieu_prise_en_charge or "—"

    def get_structure_region(self, obj):
        return obj.demande.ville.region.nom if obj.demande.ville else "—"

    def get_structure_ville(self, obj):
        return obj.demande.ville.nom if obj.demande.ville else "—"
# =====================================================
# SERIALIZER : donneurs d'une structure
# =====================================================

class DonneurStructureSerializer(serializers.Serializer):
    """
    Représente un donneur qui a interagi avec une structure
    (soit via une sollicitation, soit via une participation).

    """
    id = serializers.IntegerField()
    nom = serializers.CharField()
    prenom = serializers.CharField()
    groupe_sanguin = serializers.CharField()
    telephone = serializers.CharField()
    initiales = serializers.CharField()
    nombre_sollicitations = serializers.IntegerField()
    nombre_participations = serializers.IntegerField()
    derniere_interaction = serializers.DateTimeField()
    ville = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()

    def get_ville(self, obj):
        # obj peut être un dict (construit manuellement dans la vue)
        # ou un objet ProfilDonneur
        if isinstance(obj, dict):
            return obj.get('ville', '—')
        return obj.ville.nom if obj.ville else "—"

    def get_region(self, obj):
        if isinstance(obj, dict):
            return obj.get('region', '—')
        return obj.ville.region.nom if obj.ville else "—"

# =====================================================
# SERIALIZER : demande urgente sans compte (PUBLIC)
# =====================================================

class DemandeUrgentePublicSerializer(serializers.Serializer):
    """
    Valide la création d'une demande urgente par une personne
    sans compte (type_createur = PUBLIC).
    """

    # ---- Champs avec validation DRF native ----

    groupe_sanguin = serializers.ChoiceField(choices=Demande.GroupeSanguin.choices,  error_messages={
        'invalid_choice': "Veuillez choisir un groupe sanguin.",
    },)
    urgence = serializers.ChoiceField(choices=Demande.Urgence.choices, error_messages={
        'invalid_choice': "Veuillez choisir le niveau d'urgence.",
    },)

    ville_id = serializers.PrimaryKeyRelatedField(
        queryset=Ville.objects.all(),
        source='ville',
    )

    latitude_urgence = serializers.FloatField(
        required=False, allow_null=True, min_value=-90, max_value=90,
    )
    longitude_urgence = serializers.FloatField(
        required=False, allow_null=True, min_value=-180, max_value=180,
    )

    message = serializers.CharField(required=False, allow_blank=True, max_length=1000)

    email_demandeur = serializers.EmailField()

    # ---- Champs avec validation custom ----

    quantite = serializers.IntegerField()
    telephone_demandeur = serializers.CharField(max_length=20)
    nom_demandeur = serializers.CharField(max_length=200)
    nom_patient = serializers.CharField(max_length=200)
    lieu_prise_en_charge = serializers.CharField(max_length=255)

    # ==========================================
    # VALIDATEURS
    # ==========================================

    def validate_quantite(self, value):
        """Quantité entre 1 et 50 poches."""
        if value < 1:
            raise serializers.ValidationError("La quantité doit être d'au moins 1 poche.")
        if value > 50:
            raise serializers.ValidationError("La quantité ne peut pas dépasser 50 poches.")
        return value

    def validate_telephone_demandeur(self, value):
        """Téléphone sénégalais normalisé."""
        from accounts.constants import normaliser_telephone
        try:
            return normaliser_telephone(value)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def validate_nom_demandeur(self, value):
        """Lettres uniquement + longueur min/max."""
        from accounts.constants import valider_nom_propre
        try:
            return valider_nom_propre(value, 'le nom du demandeur', min_length=2, max_length=200)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def validate_nom_patient(self, value):
        """Lettres uniquement + longueur min/max."""
        from accounts.constants import valider_nom_propre
        try:
            return valider_nom_propre(value, 'le nom du patient', min_length=2, max_length=200)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def validate_lieu_prise_en_charge(self, value):
        """Lieu : 3 à 255 caractères."""
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError(
                "Le lieu de prise en charge doit contenir au moins 3 caractères."
            )
        if len(value) > 255:
            raise serializers.ValidationError(
                "Le lieu de prise en charge ne peut pas dépasser 255 caractères."
            )
        return value

    def validate_email_demandeur(self, value):
        """Normalise l'email en minuscules."""
        return value.strip().lower()

    # ==========================================
    # CRÉATION
    # ==========================================

    def create(self, validated_data):
        token = secrets.token_urlsafe(48)
        date_limite = timezone.now() + timedelta(hours=24)

        return Demande.objects.create(
            type_createur=Demande.TypeCreateur.PUBLIC,
            ville=validated_data['ville'],
            groupe_sanguin=validated_data['groupe_sanguin'],
            quantite=validated_data['quantite'],
            urgence=validated_data['urgence'],
            message=validated_data.get('message', ''),
            statut=Demande.StatutDemande.EN_VERIFICATION,
            date_limite=date_limite,
            nom_demandeur=validated_data['nom_demandeur'],
            telephone_demandeur=validated_data['telephone_demandeur'],
            email_demandeur=validated_data['email_demandeur'],
            nom_patient=validated_data['nom_patient'],
            lieu_prise_en_charge=validated_data['lieu_prise_en_charge'],
            token_suivi=token,
            latitude_urgence=validated_data.get('latitude_urgence'),
            longitude_urgence=validated_data.get('longitude_urgence'),
        )