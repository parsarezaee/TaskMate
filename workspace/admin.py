from django.contrib import admin
from .models import Workspace, Membership



@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'unique_code', 'description', 'visibility')
    list_filter = ('visibility',)
    search_fields = ('name', 'unique_code', 'owner__email')
    readonly_fields = ('unique_code',)


@admin.register(Membership)
class MemberShipAdmin(admin.ModelAdmin):
    list_display = ('user', 'workspace', 'role')
    list_filter = ('role', 'workspace')
    search_fields = ('user__email', 'workspace__name')