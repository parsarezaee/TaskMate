from django.urls import path
from . import views
urlpatterns = [
    path('create/', views.WorkspaceListCreateView.as_view(), name='workspace-list-create'),
    path('workspace/<int:pk>/', views.WorkspaceRetrieveUpdateDeleteView.as_view(), name='workspace-detail-update-delete'),
    path('workspace/<int:workspace_id>/add-member/', views.AddMemberToWorkspaceView.as_view(), name='add_member_to_workspace'),
    path('workspace/<int:workspace_id>/transfer-ownership/', views.TransferOwnershipView.as_view(), name='transfer_ownership'),
    path('workspace/<int:workspace_id>/leave/', views.LeaveWorkspaceView.as_view(), name='leave_workspace'),
    path('workspace/<int:workspace_id>/remove-member/', views.RemoveMemberView.as_view(), name='remove_member'),
]
