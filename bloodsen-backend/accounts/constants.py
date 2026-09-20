import re


# =====================================================
# RÉGIONS DU SÉNÉGAL
# =====================================================
# Liste officielle des 14 régions du Sénégal.
# Utilisée pour valider les inscriptions (donneur + structure).
REGIONS_SENEGAL = [
    'Dakar',
    'Diourbel',
    'Fatick',
    'Kaffrine',
    'Kaolack',
    'Kédougou',
    'Kolda',
    'Louga',
    'Matam',
    'Saint-Louis',
    'Sédhiou',
    'Tambacounda',
    'Thiès',
    'Ziguinchor',
]

# Choix prêts à l'emploi pour les serializers
REGIONS_CHOICES = [(r, r) for r in REGIONS_SENEGAL]


# =====================================================
# NORMALISATION DU TÉLÉPHONE
# =====================================================
def normaliser_telephone(telephone):
    """
    Normalise un numéro de téléphone sénégalais au format standard
    "+221XXXXXXXXX" (12 caractères commençant par +221).

    Accepte plusieurs formats en entrée :
      - "+221771234567"
      - "771234567"
      - "+221 77 123 45 67"
      - "77 123 45 67"
      - "00221771234567"

    Renvoie le numéro normalisé, ou lève ValueError si le format
    n'est pas reconnu.
    """
    if not telephone:
        raise ValueError("Le numéro de téléphone est obligatoire.")

    # 1. Retirer tous les espaces, tirets, parenthèses
    nettoye = re.sub(r'[\s\-\(\)]', '', telephone)

    # 2. Retirer le préfixe international "00221" s'il existe
    if nettoye.startswith('00221'):
        nettoye = nettoye[5:]

    # 3. Retirer le préfixe "+221" s'il existe
    if nettoye.startswith('+221'):
        nettoye = nettoye[4:]

    # 4. À ce stade, on doit avoir 9 chiffres (format sénégalais)
    if not re.match(r'^7[05678]\d{7}$', nettoye):
        raise ValueError(
            "Numéro de téléphone sénégalais invalide. "
            "Format attendu : +221 7X XXX XX XX (ex: +221771234567)."
        )

    # 5. Renvoyer avec le préfixe international
    return f"+221{nettoye}"


# =====================================================
# VALIDATION DES NOMS PROPRES
# =====================================================
def valider_nom_propre(valeur, nom_du_champ='ce champ', min_length=2, max_length=100):
    """
    Valide un nom propre (nom, prénom, nom de structure...).

    Règles :
      - Minimum `min_length` caractères
      - Maximum `max_length` caractères
      - Uniquement lettres (accents autorisés), espaces, tirets, apostrophes
      - Ne peut pas être composé uniquement d'espaces
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

    # Regex : lettres (y compris accentuées), espaces, tirets, apostrophes
    if not re.match(r"^[a-zA-ZÀ-ÿ\s\-']+$", valeur):
        raise ValueError(
            f"{nom_du_champ.capitalize()} ne peut contenir que des lettres, "
            f"espaces, tirets et apostrophes."
        )

    return valeur