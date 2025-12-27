from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Board(models.Model):
    """Representa um quadro Kanban (ex: Projeto X)."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Column(models.Model):
    """Coluna dentro de um quadro (ex: To Do, Doing, Done)."""
    board = models.ForeignKey(Board, related_name="columns", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    position = models.PositiveIntegerField(default=0)  # para ordenar

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return f"{self.title} ({self.board.title})"


class Card(models.Model):
    """Cartão/tarefa dentro de uma coluna."""
    PRIORITY_CHOICES = [
        ('low', 'Baixa'),
        ('medium', 'Média'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    ]
    
    column = models.ForeignKey(Column, related_name="cards", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(default=timezone.now)
    position = models.PositiveIntegerField(default=0)  # para ordenar dentro da coluna
    is_done = models.BooleanField(default=False)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Comentário em um cartão."""
    card = models.ForeignKey(Card, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.user.username} on {self.card.title}"
