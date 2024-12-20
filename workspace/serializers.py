from rest_framework import serializers 
from .models import Workspace, Membership
from django.contrib.auth import get_user_model

User = get_user_model()



class WorkspaceSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    member_count = serializers.IntegerField(source='member_count', read_only=True)

    class Meta:
        model = Workspace
        fields = ['id', 'name', 'description', 'unique_code', 'owner', 'role', 'visibility', 'member_count']
        read_only_fields = ['id', 'unique_code', 'owner', 'role']

    def get_role(self, obj):
        user = self.context['request'].user
        try:
            membership = Membership.objects.get(workspace=obj, user=user)
            return membership.role
        except Membership.DoesNotExist:
            return None 