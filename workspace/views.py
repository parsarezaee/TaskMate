from rest_framework import generics
from .models import Workspace, Membership
from .serializers import WorkspaceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

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
        

class LeaveWorkspaceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, workspace_id):
        workspace = get_object_or_404( Workspace, id=workspace_id)

        try:
            membership = Membership.objects.get(workspace=workspace, user=request.user)
        except Membership.DoesNotExist:
            return Response({"error": "You are not a member of this workspace"}, status=status.HTTP_403_FORBIDDEN)
        
        if membership.role == "owner":
            return Response({"error": "Owner cannot leave the workspace directly"}, status=status.HTTP_400_BAD_REQUEST)
        
        membership.delete()
        return Response({"message": "You have left the workspace successfuly,"}, status=status.HTTP_200_OK)
    

class RemoveMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, workspace_id):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        workspace = get_object_or_404(Workspace, id=workspace_id)
        
        try:
            request_membership = Membership.objects.get(workspace=workspace, user=request.user)
        except Membership.DoesNotExist:
            return Response({"error": "You are not a member of this workspace"}, status=status.HTTP_403_FORBIDDEN)
        
        if request_membership.role == "member":
            return Response({"error": "Members cannot remove other users"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user_to_remove = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        try:
            target_membership = Membership.objects.get(workspace=workspace, user=user_to_remove)
        except Membership.DoesNotExist:
            return Response({"error": "User is not a member of this workspace"}, status=status.HTTP_400_BAD_REQUEST)

        if target_membership.role == 'owner': 
            return Response({"error": "You cannot remove the owner"}, status=status.HTTP_403_FORBIDDEN)
        
        if request_membership.role == 'admin':
            if not request_membership.can_remove_users:
                return Response({"error": "You do not have permission to remove users"}, status=status.HTTP_403_FORBIDDEN)

        target_membership.delete()
        return Response({"message": f"User {email} removed successfully"}, status=status.HTTP_200_OK)


        