from django.contrib import admin
from .models import Workspace, Membership



@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'unique_code', 'description')
    list_filter = ('admin',)
    search_fields = ('name', 'unique_code', 'admin__email')
    readonly_fields = ('unique_code',)


@admin.register(Membership)
class MemberShipAdmin(admin.ModelAdmin):
    list_display = ('user', 'workspace', 'role')
    list_filter = ('role', 'workspace')
    search_fields = ('user__email', 'workspace__name')