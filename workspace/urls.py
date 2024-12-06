from django.urls import path
from .views import WorkspaceListCreateView, WorkspaceRetrieveUpdateDeleteView, AddMemberToWorkspaceView

urlpatterns = [
    path('create/', WorkspaceListCreateView.as_view(), name='workspace-list-create'),
    path('workspace/<int:pk>/', WorkspaceRetrieveUpdateDeleteView.as_view(), name='workspace-detail-update-delete'),
    path('workspace/<int:workspace_id>/add-member/', AddMemberToWorkspaceView.as_view(), name='add_member_to_workspace'),
]
