from rest_framework import generics
from .models import Workspace, Membership
from .serializers import WorkspaceSerializer
from rest_framework.permissions import IsAuthenticated



class WorkspaceListCreateView(generics.ListCreateAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        workspace = serializer.save(admin=self.request.user)
        Membership.objects.create(user=self.request.user, workspace=workspace, role="admin")


class WorkspaceRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Workspace.objects.filter(membership__user=self.request.user)