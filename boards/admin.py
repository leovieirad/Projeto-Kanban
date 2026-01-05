from django.contrib import admin
from .models import Board, Column, Card, Comment, Activity, BoardMember

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'created_at']
    list_filter = ['owner']
    search_fields = ['title', 'description']

@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ['title', 'board', 'position']
    list_filter = ['board']
    search_fields = ['title']

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['title', 'column', 'priority', 'created_at', 'is_done']
    list_filter = ['priority', 'is_done', 'column__board']
    search_fields = ['title', 'description']
    list_editable = ['priority', 'is_done']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['card', 'user', 'text_preview', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['text', 'card__title', 'user__username']
    readonly_fields = ['created_at']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Comentário'

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['card', 'user', 'get_action', 'timestamp']
    list_filter = ['action', 'timestamp', 'user']
    search_fields = ['card__title', 'user__username', 'description']
    readonly_fields = ['card', 'user', 'action', 'description', 'timestamp']
    
    def get_action(self, obj):
        return obj.get_action_display()
    get_action.short_description = 'Ação'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
    list_display = ['board', 'user', 'role']
    list_filter = ['role', 'board']
    search_fields = ['board__title', 'user__username', 'user__email']
