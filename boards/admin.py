from django.contrib import admin
from .models import Board, Column, Card

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
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
