import cohere
from django.conf import settings
from pypdf import PdfReader
from pgvector.django import CosineDistance
from groq import Groq



from .models import Document, DocumentChunk


# =====================================================
# 1. Extraction du texte depuis un PDF
# =====================================================

def extraire_texte_pdf(chemin_pdf):
    """
    Lit un fichier PDF et renvoie tout son texte concaténé.

    Utilise pypdf pour extraire page par page, puis joint les pages
    avec un double saut de ligne (pour garder une séparation logique).
    """
    lecteur = PdfReader(chemin_pdf)
    pages = []
    for page in lecteur.pages:
        texte = page.extract_text() or ''   # extract_text peut renvoyer None
        pages.append(texte)
    return '\n\n'.join(pages)


# =====================================================
# 2. Découpage en chunks
# =====================================================

def decouper_en_chunks(texte, taille=500, overlap=50):
    """
    Découpe un texte en morceaux d'environ `taille` mots, avec un
    chevauchement de `overlap` mots entre deux chunks consécutifs.

    Le chevauchement évite de couper une idée importante en plein
    milieu : si une phrase est à cheval sur deux chunks, elle
    apparaîtra en entier dans au moins un des deux.

    Renvoie une liste de chaînes de caractères.
    """
    # On découpe d'abord par mots (approximation simple : split sur espaces)
    mots = texte.split()

    chunks = []
    debut = 0
    while debut < len(mots):
        fin = debut + taille
        chunk_mots = mots[debut:fin]
        chunks.append(' '.join(chunk_mots))

        # Avancer de `taille - overlap` pour créer le chevauchement.
        # Ex : taille=500, overlap=50 → on avance de 450 à chaque itération.
        debut += (taille - overlap)

        # Si on est déjà au bout, on s'arrête
        if fin >= len(mots):
            break

    return chunks


# =====================================================
# 3. Vectorisation via Cohere
# =====================================================

def vectoriser_textes(liste_textes):
    """
    Prend une liste de textes et renvoie une liste de vecteurs
    (un vecteur de 1024 floats par texte).

    Utilise l'API Cohere. Le paramètre input_type='search_document'
    est recommandé pour les documents qu'on va ensuite rechercher.
    Pour les questions, on utilisera 'search_query'.
    """
    client = cohere.Client(api_key=settings.COHERE_API_KEY)

    reponse = client.embed(
        texts=liste_textes,
        model=settings.COHERE_EMBED_MODEL,
        input_type='search_document',
    )

    # reponse.embeddings est une liste de listes de floats
    return reponse.embeddings


# =====================================================
# 4. Fonction principale : ingérer un document
# =====================================================

def ingerer_document(document):
    """
    Chaîne complète d'ingestion :
      1. Extraire le texte du PDF
      2. Découper en chunks
      3. Vectoriser les chunks
      4. Créer les DocumentChunk en base

    Si des chunks existent déjà pour ce document (cas d'une ré-ingestion),
    ils sont d'abord supprimés pour éviter les doublons.

    Renvoie le nombre de chunks créés.
    """
    # 1. Extraire le texte
    chemin = document.fichier.path
    texte = extraire_texte_pdf(chemin)

    if not texte.strip():
        raise ValueError(
            f"Le PDF « {document.titre} » ne contient pas de texte extractible "
            f"(peut-être un PDF scanné/image)."
        )

    # 2. Découper en chunks
    chunks = decouper_en_chunks(
        texte,
        taille=settings.RAG_CHUNK_SIZE,
        overlap=settings.RAG_CHUNK_OVERLAP,
    )

    # 3. Supprimer les anciens chunks (cas d'une ré-ingestion)
    DocumentChunk.objects.filter(document=document).delete()

    # 4. Vectoriser par lots (Cohere accepte jusqu'à 96 textes par appel)
    #    On découpe en lots de 90 pour rester sous la limite.
    tous_vecteurs = []
    taille_lot = 90
    for i in range(0, len(chunks), taille_lot):
        lot = chunks[i:i + taille_lot]
        vecteurs = vectoriser_textes(lot)
        tous_vecteurs.extend(vecteurs)

    # 5. Créer les DocumentChunk en base
    objets = [
        DocumentChunk(
            document=document,
            contenu=chunk,
            ordre=i,
            embedding=vecteur,
        )
        for i, (chunk, vecteur) in enumerate(zip(chunks, tous_vecteurs))
    ]

    DocumentChunk.objects.bulk_create(objets)

    return len(objets)

# =====================================================
# 5. Vectorisation d'une question utilisateur
# =====================================================

def vectoriser_question(question):
    """
    Vectorise une question utilisateur.

    Différence cruciale avec vectoriser_textes() : on utilise
    input_type='search_query' au lieu de 'search_document'.
    Cohere entraîne ses modèles avec ces deux modes distincts,
    et utiliser le bon mode améliore la qualité de la recherche.
    """
    client = cohere.Client(api_key=settings.COHERE_API_KEY)

    reponse = client.embed(
        texts=[question],
        model=settings.COHERE_EMBED_MODEL,
        input_type='search_query',
    )

    # On renvoie le premier (et unique) vecteur
    return reponse.embeddings[0]


# =====================================================
# 6. Recherche des chunks les plus similaires
# =====================================================

def rechercher_chunks_similaires(vecteur_question, limite=5, seuil=0.5):
    """
    Cherche les chunks les plus proches sémantiquement du vecteur
    d'une question, en utilisant la distance cosinus.

    Paramètres :
      - vecteur_question : liste de 1024 floats
      - limite : nombre maximum de chunks à renvoyer
      - seuil : distance cosinus max (0 = identique, 1 = orthogonal)
                Les chunks dont la distance est >= seuil sont exclus.

    Renvoie un QuerySet de DocumentChunk triés par distance croissante.
    """

    chunks = (
        DocumentChunk.objects
        .filter(document__actif=True)
        .annotate(distance=CosineDistance('embedding', vecteur_question))
        .filter(distance__lt=seuil)
        .order_by('distance')[:limite]
    )
    return list(chunks)


# =====================================================
# 7. Construction du contexte pour le LLM
# =====================================================

def construire_contexte(chunks):
    """
    Assemble les chunks trouvés en un texte unique structuré,
    à envoyer au LLM comme contexte.

    Format :
        [Source 1 : <titre du document>]
        <contenu du chunk 1>

        [Source 2 : <titre du document>]
        <contenu du chunk 2>

        ---

    Renvoie une chaîne de caractères (vide si aucun chunk).
    """
    if not chunks:
        return ''

    blocs = []
    for i, chunk in enumerate(chunks, start=1):
        titre = chunk.document.titre
        blocs.append(
            f"[Source {i} : {titre}]\n{chunk.contenu}"
        )

    return '\n\n'.join(blocs) + '\n\n---'


# =====================================================
# 8. Génération de réponse via Groq
# =====================================================

def generer_reponse(question, contexte):
    """
    Envoie à Groq le contexte + la question, et renvoie la réponse
    générée par le LLM.

    Le prompt système est strict : le LLM doit répondre UNIQUEMENT
    à partir du contexte fourni, sinon il doit dire qu'il ne sait pas.
    """

    client = Groq(api_key=settings.GROQ_API_KEY)

    prompt_systeme = (
        "Tu es un assistant spécialisé dans le don de sang pour la plateforme BloodSen.\n\n"
        "RÈGLES STRICTES :\n"
        "1. Réponds UNIQUEMENT à partir des informations du CONTEXTE ci-dessous.\n"
        "2. Si le contexte ne contient pas l'information nécessaire, réponds EXACTEMENT :\n"
        "   « Je n'ai pas d'information sur cette question. Consultez un professionnel de santé pour plus de détails. »\n"
        "3. N'invente JAMAIS d'information. N'utilise PAS tes connaissances générales.\n"
        "4. Réponds en français, de manière claire et concise.\n"
        "5. Si pertinent, cite la source (ex: « Selon le Guide du don de sang... »).\n"
    )

    prompt_utilisateur = (
        f"CONTEXTE :\n{contexte}\n\n"
        f"QUESTION DE L'UTILISATEUR :\n{question}\n\n"
        f"Réponse :"
    )

    reponse = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": prompt_systeme},
            {"role": "user", "content": prompt_utilisateur},
        ],
        temperature=0.2,   # peu créatif = plus factuel
        max_tokens=1024,
    )

    return reponse.choices[0].message.content


# =====================================================
# 9. Fonction principale : répondre à une question
# =====================================================

def repondre_question(question):
    """
    Pipeline complet du RAG :
      1. Vectoriser la question
      2. Chercher les chunks similaires
      3. Si aucun chunk → réponse par défaut
      4. Sinon → construire le contexte, appeler le LLM, renvoyer

    Renvoie un dictionnaire :
        {
            "reponse": str,
            "sources": [liste des titres de documents utilisés],
            "trouve": bool,   # False si rien de pertinent n'a été trouvé
        }
    """
    # 1. Vectoriser la question
    vecteur = vectoriser_question(question)

    # 2. Chercher les chunks similaires
    chunks = rechercher_chunks_similaires(
        vecteur,
        limite=settings.RAG_MAX_CHUNKS,
        seuil=settings.RAG_SIMILARITY_THRESHOLD,
    )

    # 3. Aucun chunk pertinent → réponse par défaut
    if not chunks:
        return {
            "reponse": (
                "Je n'ai pas d'information sur cette question. "
                "Consultez un professionnel de santé pour plus de détails."
            ),
            "sources": [],
            "trouve": False,
        }

    # 4. Construire le contexte et appeler le LLM
    contexte = construire_contexte(chunks)
    reponse = generer_reponse(question, contexte)

    # 5. Extraire la liste unique des titres de documents utilisés
    titres = list({chunk.document.titre for chunk in chunks})

    return {
        "reponse": reponse,
        "sources": titres,
        "trouve": True,
    }