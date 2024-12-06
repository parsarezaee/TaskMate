from rest_framework import generics
from .models import Workspace, Membership
from .serializers import WorkspaceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

User = get_user_model()



class WorkspaceListCreateView(generics.ListCreateAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        workspace = serializer.save(owner=self.request.user)
        Membership.objects.create(user=self.request.user, workspace=workspace, role="owner")


class WorkspaceRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Workspace.objects.filter(membership__user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Workspace deleted successfully."}, status=status.HTTP_200_OK)


class AddMemberToWorkspaceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, workspace_id):
        email = request.data.get('email')
        role = request.data.get('role', 'member')

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            workspace = Workspace.objects.get(id=workspace_id)
        except Workspace.DoesNotExist:
            return Response({"error": "Workspace not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            membership = Membership.objects.get(workspace=workspace, user=request.user)
            if membership.role not in ["owner", "admin"]:
                return Response({"error": "Only owners or admins can add members"}, status=status.HTTP_403_FORBIDDEN)
        except Membership.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            user_to_add = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if Membership.objects.filter(workspace=workspace, user=user_to_add).exists():
            return Response({"error": "User is already a member of this workspace"}, status=status.HTTP_400_BAD_REQUEST)

        Membership.objects.create(workspace=workspace, user=user_to_add, role=role)
        return Response({"message": f"User {email} added to the workspace successfully"}, status=status.HTTP_201_CREATED)
        
        