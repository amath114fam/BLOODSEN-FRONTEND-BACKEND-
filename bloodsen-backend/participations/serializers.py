from rest_framework import serializers

from .models import Participation
from demandes.models import Sollicitation




class ParticipationSerializer(serializers.ModelSerializer):
    """
    Serializer utilisé pour LIRE une participation.

    Comme pour les autres serializers, on enrichit avec des infos
    utiles au frontend : donneur, structure, demande associée.
    """

    donneur_nom = serializers.CharField(
        source='sollicitation.donneur.nom',
        read_only=True,
    )
    donneur_prenom = serializers.CharField(
        source='sollicitation.donneur.prenom',
        read_only=True,
    )
    donneur_groupe_sanguin = serializers.CharField(
        source='sollicitation.donneur.groupe_sanguin',
        read_only=True,
    )
    demande_id = serializers.IntegerField(
        source='sollicitation.demande.id',
        read_only=True,
    )
    structure_nom = serializers.CharField(
        source='sollicitation.demande.structure.nom_structure',
        read_only=True,
    )

    class Meta:
        model = Participation
        fields = [
            'id',
            'donneur_nom',
            'donneur_prenom',
            'donneur_groupe_sanguin',
            'demande_id',
            'structure_nom',
            'statut',
            'date_confirmation',
        ]

# =====================================================
# SERIALIZER : participations d'une structure
# =====================================================

# =====================================================
# SERIALIZER : sollicitations/participations d'une structure
# =====================================================

class SollicitationStructureSerializer(serializers.ModelSerializer):
    """
    Représente une sollicitation vue par une structure, avec :
      - les infos du donneur
      - les infos de la demande associée
      - le statut de la sollicitation
      - les infos de la participation (si elle existe)

    Le champ "statut_affiche" est une version combinée :
      - 'pending'         : sollicitation en attente ou acceptée sans confirmation
      - 'confirmed'       : participation confirmée
      - 'medical_refusal' : sollicitation refusée
      - 'cancelled'       : participation annulée
    """
    # Infos du donneur
    donneur_nom = serializers.CharField(
        source='donneur.nom',
        read_only=True,
    )
    donneur_prenom = serializers.CharField(
        source='donneur.prenom',
        read_only=True,
    )
    donneur_groupe_sanguin = serializers.CharField(
        source='donneur.groupe_sanguin',
        read_only=True,
    )
    donneur_ville = serializers.CharField(
        source='donneur.ville',
        read_only=True,
    )
    donneur_initiales = serializers.SerializerMethodField()

    # Infos de la demande
    demande_id = serializers.IntegerField(
        source='demande.id',
        read_only=True,
    )
    demande_reference = serializers.SerializerMethodField()
    demande_message = serializers.CharField(
        source='demande.message',
        read_only=True,
    )
    demande_groupe_sanguin = serializers.CharField(
        source='demande.groupe_sanguin',
        read_only=True,
    )

    # Statut affiché (calculé)
    statut_affiche = serializers.SerializerMethodField()

    # Infos de la participation (si elle existe)
    date_confirmation = serializers.SerializerMethodField()

    class Meta:
        model = Sollicitation
        fields = [
            'id',
            'donneur_nom',
            'donneur_prenom',
            'donneur_initiales',
            'donneur_groupe_sanguin',
            'donneur_ville',
            'demande_id',
            'demande_reference',
            'demande_message',
            'demande_groupe_sanguin',
            'statut',
            'statut_affiche',
            'date_creation',
            'date_reponse',
            'date_confirmation',
        ]

    def get_donneur_initiales(self, obj):
        prenom = obj.donneur.prenom or ''
        nom = obj.donneur.nom or ''
        return ((prenom[:1] + nom[:1]).upper()) or '?'

    def get_demande_reference(self, obj):
        return f"#DS-{obj.demande.id:04d}"

    def get_statut_affiche(self, obj):
        """
        Combine le statut de la sollicitation et l'existence
        d'une participation pour produire un statut unique.
        """
        # Y a-t-il une participation liée ?
        if hasattr(obj, 'participation'):
            if obj.participation.statut == 'confirmee':
                return 'confirmed'
            if obj.participation.statut == 'annulee':
                return 'cancelled'

        # Sinon, on regarde le statut de la sollicitation
        if obj.statut == 'refusee':
            return 'medical_refusal'
        if obj.statut == 'acceptee':
            return 'pending'   # acceptée mais pas encore confirmée
        return 'pending'       # en attente

    def get_date_confirmation(self, obj):
        if hasattr(obj, 'participation'):
            return obj.participation.date_confirmation
        return None