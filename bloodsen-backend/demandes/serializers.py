from rest_framework import serializers

from .models import Demande, Sollicitation
from participations.models import Participation

from django.utils import timezone
from datetime import timedelta

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
    Serializer utilisé pour LIRE une demande (GET).
    """

    structure_nom = serializers.CharField(
        source='structure.nom_structure',
        read_only=True,
    )
    structure_region = serializers.CharField(
        source='structure.region',
        read_only=True,
    )
    structure_ville = serializers.CharField(
        source='structure.ville',
        read_only=True,
    )
    nombre_sollicitations = serializers.IntegerField(
        source='sollicitations.count',
        read_only=True,
    )
    # Nombre de sollicitations encore en attente (non traitées)
    nombre_sollicitations_en_attente = serializers.SerializerMethodField()
    # Nombre de participations confirmées
    nombre_participations_confirmees = serializers.SerializerMethodField()

    class Meta:
        model = Demande
        fields = [
            'id',
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

    def get_nombre_sollicitations_en_attente(self, obj):
        """Compte les sollicitations avec statut "en_attente"."""
        return obj.sollicitations.filter(statut='en_attente').count()

    def get_nombre_participations_confirmees(self, obj):
        """Compte les participations confirmées liées aux sollicitations de cette demande."""
        return Participation.objects.filter(
            sollicitation__demande=obj,
            statut='confirmee',
        ).count()

class SollicitationSerializer(serializers.ModelSerializer):
    """
    Serializer utilisé pour LIRE une sollicitation (GET ou après action).

    On inclut des infos utiles au donneur (le nom de la structure,
    son message) et au frontend pour l'affichage.
    """

    demande_id = serializers.IntegerField(source='demande.id', read_only=True)
    structure_nom = serializers.CharField(
        source='demande.structure.nom_structure',
        read_only=True,
    )
    structure_region = serializers.CharField(
        source='demande.structure.region',
        read_only=True,
    )
    structure_ville = serializers.CharField(
        source='demande.structure.ville',
        read_only=True,
    )
    groupe_sanguin = serializers.CharField(
        source='demande.groupe_sanguin',
        read_only=True,
    )
    urgence = serializers.CharField(
        source='demande.urgence',
        read_only=True,
    )
    message = serializers.CharField(
        source='demande.message',
        read_only=True,
    )

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
        ]

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
    ville = serializers.CharField()
    region = serializers.CharField()
    telephone = serializers.CharField()
    initiales = serializers.CharField()
    nombre_sollicitations = serializers.IntegerField()
    nombre_participations = serializers.IntegerField()
    derniere_interaction = serializers.DateTimeField()