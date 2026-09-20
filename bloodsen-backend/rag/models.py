from django.db import models
from pgvector.django import VectorField


class Document(models.Model):
    """
    Document source uploadé par un superuser.

    Représente un PDF (ou autre) contenant des informations vérifiées
    sur le don de sang. Une fois uploadé, le document est découpé en
    chunks (DocumentChunk) qui sont vectorisés et stockés.
    """
    titre = models.CharField(
        max_length=255,
        help_text="Titre lisible du document (ex: 'Guide du don de sang - OMS')",
    )
    fichier = models.FileField(
        upload_to='rag_documents/',
        help_text="Le fichier PDF uploadé",
    )
    description = models.TextField(
        blank=True,
        help_text="Description optionnelle du contenu du document",
    )
    ajoute_par = models.ForeignKey(
        'accounts.Utilisateur',
        on_delete=models.SET_NULL,
        null=True,
        related_name='documents_ajoutes',
        help_text="Superuser qui a uploadé le document",
    )
    date_ajout = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(
        default=True,
        help_text="Si False, le document n'est plus utilisé pour répondre aux questions",
    )

    class Meta:
        ordering = ['-date_ajout']

    def __str__(self):
        return self.titre


class DocumentChunk(models.Model):
    """
    Un morceau de document (chunk) avec son vecteur.

    Chaque Document est découpé en plusieurs DocumentChunk. Chaque chunk
    contient un texte (une portion du document) et son embedding (un
    vecteur de 1024 nombres) qui permet de faire de la recherche
    sémantique par similarité.
    """
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='chunks',
    )
    contenu = models.TextField(
        help_text="Le texte de ce morceau",
    )
    ordre = models.PositiveIntegerField(
        help_text="Position du chunk dans le document (0, 1, 2, ...)",
    )
    embedding = VectorField(
        dimensions=1024,
        help_text="Vecteur produit par Cohere (embed-multilingual-v3)",
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['document', 'ordre']
        # Un même document ne peut pas avoir deux chunks avec le même ordre
        unique_together = ('document', 'ordre')

    def __str__(self):
        return f"Chunk {self.ordre} de {self.document.titre}"