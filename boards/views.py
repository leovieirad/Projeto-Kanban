from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Board, Column, Card

# Listagem de quadros
class BoardListView(ListView):
    model = Board
    template_name = "boards/board_list.html"
    context_object_name = "boards"

# Detalhe de um quadro
class BoardDetailView(DetailView):
    model = Board
    template_name = "boards/board_detail.html"
    context_object_name = "board"

# Criar quadro via formulário simples
def create_board(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        if title:
            board = Board.objects.create(title=title, description=description)
            return redirect("boards:detail", pk=board.pk)
    return render(request, "boards/board_form.html", {"form_data": request.POST})

# Criar coluna dentro de um quadro
def create_column(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if title:
            position = board.columns.count()
            Column.objects.create(board=board, title=title, position=position)
    return redirect("boards:detail", pk=board.pk)

# Criar cartão dentro de uma coluna
def create_card(request, column_pk):
    column = get_object_or_404(Column, pk=column_pk)
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if title:
            position = column.cards.count()
            Card.objects.create(column=column, title=title, position=position)
    return redirect("boards:detail", pk=column.board.pk)

def update_board(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        if title:
            board.title = title
            board.description = description
            board.save()
        return redirect("boards:detail", pk=pk)
    return render(request, "boards/board_form.html", {"form_data": {"title": board.title, "description": board.description}})