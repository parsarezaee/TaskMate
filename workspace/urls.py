from django.urls import path
from .views import WorkspaceListCreateView, WorkspaceRetrieveUpdateDeleteView

urlpatterns = [
    path('create/', WorkspaceListCreateView.as_view(), name='workspace-list-create'),
    path('workspace/<int:pk>/', WorkspaceRetrieveUpdateDeleteView.as_view(), name='workspace-detail-update-delete'),
]
