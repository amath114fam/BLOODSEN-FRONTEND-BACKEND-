from rest_framework import serializers

from .models import Participation


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