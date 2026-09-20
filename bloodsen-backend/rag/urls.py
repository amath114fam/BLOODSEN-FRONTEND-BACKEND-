from django.urls import path

from .views import (
    ChatView,
    DocumentListCreateView,
    DocumentDetailView,
    DocumentReingestView,
)

urlpatterns = [
    # Chat (donneur ou structure)
    path('rag/chat/', ChatView.as_view(), name='rag-chat'),

    # Documents (admin uniquement)
    path('rag/documents/', DocumentListCreateView.as_view(), name='rag-documents'),
    path('rag/documents/<int:pk>/', DocumentDetailView.as_view(), name='rag-document-detail'),
    path('rag/documents/<int:pk>/reingerer/', DocumentReingestView.as_view(), name='rag-document-reingest'),
]