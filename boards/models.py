from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date

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
    due_date = models.DateField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_cards")
    position = models.PositiveIntegerField(default=0)  # para ordenar dentro da coluna
    is_done = models.BooleanField(default=False)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.title
    
    def get_due_date_status(self):
        """Retorna o status da data de vencimento: 'overdue', 'due-soon', 'on-time' ou None."""
        if not self.due_date:
            return None
        
        today = date.today()
        days_until_due = (self.due_date - today).days
        
        if days_until_due < 0:
            return 'overdue'
        elif days_until_due <= 3:
            return 'due-soon'
        else:
            return 'on-time'


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

class Activity(models.Model):
    """Log de atividades/alterações em cartões."""
    ACTION_CHOICES = [
        ('created', 'Criado'),
        ('title_changed', 'Título alterado'),
        ('description_changed', 'Descrição alterada'),
        ('priority_changed', 'Prioridade alterada'),
        ('assigned', 'Atribuído'),
        ('unassigned', 'Desatribuído'),
        ('due_date_changed', 'Data de vencimento alterada'),
        ('moved', 'Movido para outra coluna'),
        ('completed', 'Marcado como concluído'),
        ('reopened', 'Reabrindo'),
        ('comment_added', 'Comentário adicionado'),
        ('tag_added', 'Tag adicionada'),
        ('tag_removed', 'Tag removida'),
    ]
    
    card = models.ForeignKey(Card, related_name="activities", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField(blank=True)  # Ex: "Alterado de Média para Alta"
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name_plural = "Activities"

    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} em {self.card.title}"