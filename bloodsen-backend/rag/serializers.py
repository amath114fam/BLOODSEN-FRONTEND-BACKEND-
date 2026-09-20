from rest_framework import serializers
from .models import Document, DocumentChunk


# =====================================================
# Serializers pour le chat
# =====================================================

class ChatRequestSerializer(serializers.Serializer):
    """
    Valide la requête du chat : une question en texte.
    """
    question = serializers.CharField(
        min_length=3,
        max_length=1000,
        help_text="La question posée par l'utilisateur",
    )

    def validate_question(self, value):
        """
        Vérifie que la question n'est pas composée uniquement d'espaces.
        """
        if not value.strip():
            raise serializers.ValidationError(
                "La question ne peut pas être vide."
            )
        return value.strip()


# =====================================================
# Serializers pour les documents
# =====================================================

class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer pour la lecture des documents (GET).
    """
    nombre_chunks = serializers.IntegerField(
        source='chunks.count',
        read_only=True,
    )
    ajoute_par_email = serializers.CharField(
        source='ajoute_par.email',
        read_only=True,
    )

    class Meta:
        model = Document
        fields = [
            'id',
            'titre',
            'description',
            'fichier',
            'nombre_chunks',
            'ajoute_par_email',
            'date_ajout',
            'actif',
        ]
        read_only_fields = ['id', 'date_ajout', 'nombre_chunks', 'ajoute_par_email']


class DocumentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'upload d'un document (POST).
    Valide le type, la taille et le contenu du fichier.
    """
    TAILLE_MAX_FICHIER = 10 * 1024 * 1024  # 10 Mo en octets 
    # 1 Ko = 1024 octets
    # 1 Mo = 1024 Ko

    # On force le type FileField explicitement pour que
    # drf-spectacular génère un champ binaire dans Swagger.
    fichier = serializers.FileField(
        required=True,
        help_text="Le fichier PDF à uploader (max 10 Mo)",
    )

    class Meta:
        model = Document
        fields = ['titre', 'fichier', 'description']

    def validate_titre(self, value):
        """
        Le titre doit contenir entre 3 et 255 caractères.
        """
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Le titre doit contenir au moins 3 caractères."
            )
        if len(value) > 255:
            raise serializers.ValidationError(
                "Le titre ne peut pas dépasser 255 caractères."
            )
        return value.strip()

    def validate_description(self, value):
        """
        La description ne doit pas dépasser 500 caractères.
        """
        if value and len(value) > 500:
            raise serializers.ValidationError(
                "La description ne peut pas dépasser 500 caractères."
            )
        return value

    def validate_fichier(self, value):
        """
        Valide le fichier PDF :
          - extension .pdf
          - type MIME application/pdf
          - taille < 10 Mo
        """
        # 1. Vérifier l'extension
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError(
                "Seuls les fichiers PDF sont acceptés."
            )

        # 2. Vérifier la taille
        if value.size > self.TAILLE_MAX_FICHIER:
            taille_mo = value.size / (1024 * 1024)
            raise serializers.ValidationError(
                f"Le fichier est trop volumineux ({taille_mo:.1f} Mo). "
                f"Taille maximale autorisée : 10 Mo."
            )

        # 3. Vérifier que le fichier n'est pas vide
        if value.size == 0:
            raise serializers.ValidationError(
                "Le fichier est vide."
            )

        return value