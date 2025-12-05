from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Board, Column, Card

class BoardListView(ListView):
    model = Board
    template_name = "boards/board_list.html"
    context_object_name = "boards"

class BoardDetailView(DetailView):
    model = Board
    template_name = "boards/board_detail.html"
    context_object_name = "board"

def create_board(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        if title:
            board = Board.objects.create(title=title, description=description)
            return redirect("boards:detail", pk=board.pk)
    return render(request, "boards/board_form.html")

def create_column(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if title:
            Column.objects.create(
                board=board,
                title=title,
                position=board.columns.count()
            )
    return redirect("boards:detail", pk=board.pk)

def update_board(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == "POST":
        board.title = request.POST.get("title")
        board.description = request.POST.get("description")
        board.save()
        return redirect("boards:detail", pk=pk)

    return render(request, "boards/board_form.html", {"form_data": board})

@require_POST
def toggle_card_done(request, card_pk):
    card = get_object_or_404(Card, pk=card_pk)
    card.is_done = not card.is_done
    card.save()
    return JsonResponse({"is_done": card.is_done})

def edit_card(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    if request.method == "POST":
        card.title = request.POST.get("title")
        card.description = request.POST.get("description")
        card.save()
    return redirect("board_detail", board_id=card.column.board.id)


def create_card(request, column_id):
    column = get_object_or_404(Column, id=column_id)
    if request.method == "POST":
        Card.objects.create(
            column=column,
            title=request.POST.get("title"),
            description=request.POST.get("description")
        )
    return redirect("board_detail", board_id=column.board.id)

