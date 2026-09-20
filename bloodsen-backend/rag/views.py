from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Document
from .serializers import (
    ChatRequestSerializer,
    DocumentSerializer,
    DocumentCreateSerializer,
)
from .services import repondre_question, ingerer_document


# =====================================================
# Vue 1 : Chat (poser une question au chatbot)
# =====================================================

@extend_schema(
    request=ChatRequestSerializer,
    responses=None,
    description="Pose une question au chatbot RAG sur le don de sang.",
)
class ChatView(APIView):
    """
    POST /api/rag/chat/

    Reçoit une question, la traite via le pipeline RAG
    (vectorisation → recherche → génération), et renvoie la réponse.

    Accessible aux donneurs ET aux structures authentifiés.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 1. Valider la requête
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.validated_data['question']

        # 2. Lancer le pipeline RAG
        try:
            resultat = repondre_question(question)
        except Exception as e:
            return Response(
                {"detail": f"Erreur lors du traitement de la question : {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # 3. Renvoyer le résultat
        return Response(
            {
                "question": question,
                "reponse": resultat['reponse'],
                "sources": resultat['sources'],
                "trouve": resultat['trouve'],
            },
            status=status.HTTP_200_OK,
        )


# =====================================================
# Vue 2 : Liste et création des documents (admin)
# =====================================================

@extend_schema_view(
    get=extend_schema(
        responses=DocumentSerializer(many=True),
        description="Liste tous les documents RAG (admin uniquement).",
    ),
    post=extend_schema(
        request={
            "multipart/form-data": DocumentCreateSerializer,
        },
        responses=DocumentSerializer,
        description="Upload un nouveau document (admin uniquement).",
    ),
)
class DocumentListCreateView(generics.GenericAPIView):
    """
    GET  /api/rag/documents/  → liste tous les documents
    POST /api/rag/documents/  → upload un nouveau document (déclenche l'ingestion)

    Réservé aux superusers.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DocumentCreateSerializer
        return DocumentSerializer

    def get(self, request):
        documents = Document.objects.all().order_by('-date_ajout')
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # 1. Valider les données (titre + fichier + description optionnelle)
        serializer = DocumentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Enregistrer le document (le fichier est copié dans /app/media/)
        document = serializer.save(ajoute_par=request.user)

        # 3. Lancer l'ingestion (extraction, chunking, vectorisation)
        try:
            nb_chunks = ingerer_document(document)
        except Exception as e:
            # Si l'ingestion échoue, on supprime le document pour ne pas
            # laisser un document sans chunks en base.
            document.delete()
            return Response(
                {"detail": f"Erreur lors de l'ingestion : {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # 4. Renvoyer le document créé (avec le nombre de chunks)
        response_serializer = DocumentSerializer(document)
        return Response(
            {
                **response_serializer.data,
                "chunks_crees": nb_chunks,
            },
            status=status.HTTP_201_CREATED,
        )


# =====================================================
# Vue 3 : Détail et suppression d'un document (admin)
# =====================================================

@extend_schema(
    responses=DocumentSerializer,
    description="Détail ou suppression d'un document RAG (admin uniquement).",
)
class DocumentDetailView(generics.GenericAPIView):
    """
    GET    /api/rag/documents/<id>/  → détail d'un document
    DELETE /api/rag/documents/<id>/  → supprime un document + ses chunks

    Réservé aux superusers.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        return DocumentSerializer

    def get(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        serializer = DocumentSerializer(document)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        # La suppression est en cascade : les DocumentChunk liés sont aussi supprimés
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# =====================================================
# Vue 4 : Ré-ingérer un document (admin)
# =====================================================

@extend_schema(
    request=None,
    responses=DocumentSerializer,
    description="Relance l'ingestion d'un document existant (admin uniquement).",
)
class DocumentReingestView(APIView):
    """
    POST /api/rag/documents/<id>/reingerer/

    Relance l'ingestion d'un document existant : les anciens chunks sont
    supprimés, le PDF est relu, et de nouveaux chunks sont créés.

    Utile quand on a modifié le PDF ou la logique de chunking.
    Réservé aux superusers.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, pk):
        document = get_object_or_404(Document, pk=pk)

        try:
            nb_chunks = ingerer_document(document)
        except Exception as e:
            return Response(
                {"detail": f"Erreur lors de la ré-ingestion : {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        serializer = DocumentSerializer(document)
        return Response(
            {
                **serializer.data,
                "chunks_crees": nb_chunks,
            },
            status=status.HTTP_200_OK,
        )