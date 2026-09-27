import re
from rest_framework import serializers
from .models import MessageContact


# =====================================================
# FONCTIONS DE VALIDATION
# =====================================================

def valider_nom_propre(valeur, nom_du_champ='ce champ', min_length=2, max_length=200):
    """
    Valide un nom propre (lettres, espaces, tirets, apostrophes).
    """
    if not valeur or not valeur.strip():
        raise ValueError(f"{nom_du_champ.capitalize()} est obligatoire.")

    valeur = valeur.strip()

    if len(valeur) < min_length:
        raise ValueError(
            f"{nom_du_champ.capitalize()} doit contenir au moins {min_length} caractères."
        )

    if len(valeur) > max_length:
        raise ValueError(
            f"{nom_du_champ.capitalize()} ne peut pas dépasser {max_length} caractères."
        )

    # Lettres (y compris accentuées), espaces, tirets, apostrophes
    if not re.match(r"^[a-zA-ZÀ-ÿ\s\-']+$", valeur):
        raise ValueError(
            f"{nom_du_champ.capitalize()} ne peut contenir que des lettres, "
            f"espaces, tirets et apostrophes."
        )

    return valeur


# =====================================================
# SERIALIZER : message de contact
# =====================================================

class MessageContactSerializer(serializers.ModelSerializer):
    """
    Valide les données du formulaire de contact.
    Le champ 'sujet' est traité comme un texte libre (pas comme un nom propre),
    car il peut contenir des chiffres, des points, etc.
    """

    class Meta:
        model = MessageContact
        fields = [
            'nom_complet',
            'email',
            'sujet',
            'message',
        ]

    def validate_nom_complet(self, value):
        """Valide le nom complet (lettres uniquement)."""
        try:
            return valider_nom_propre(value, 'le nom complet', min_length=2, max_length=200)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def validate_email(self, value):
        """Vérifie que l'email est valide et le normalise en minuscules."""
        if not value or not value.strip():
            raise serializers.ValidationError("L'email est obligatoire.")
        return value.strip().lower()

    def validate_sujet(self, value):
        """Valide le sujet (longueur min/max, pas d'espaces uniquement)."""
        if not value or not value.strip():
            raise serializers.ValidationError("Le sujet est obligatoire.")

        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Le sujet doit contenir au moins 3 caractères."
            )

        if len(value) > 255:
            raise serializers.ValidationError(
                "Le sujet ne peut pas dépasser 255 caractères."
            )

        return value

    def validate_message(self, value):
        """Valide le message (longueur min/max, pas d'espaces uniquement)."""
        if not value or not value.strip():
            raise serializers.ValidationError("Le message est obligatoire.")

        value = value.strip()

        if len(value) < 10:
            raise serializers.ValidationError(
                "Le message doit contenir au moins 10 caractères."
            )

        if len(value) > 2000:
            raise serializers.ValidationError(
                "Le message ne peut pas dépasser 2000 caractères."
            )

        return value