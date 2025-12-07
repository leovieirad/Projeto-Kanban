from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Board, Column, Card
import json
from django.db import transaction
from django.views.decorators.http import require_http_methods

class BoardListView(ListView):
    model = Board
    template_name = "boards/board_list.html"
    context_object_name = "boards"
    
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return qs

class BoardDetailView(DetailView):
    model = Board
    template_name = "boards/board_detail.html"
    context_object_name = "board"
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        board = self.get_object()

        # Definir colunas padrão a exibir na ordem desejada.
        desired = [
            ("A Fazer", "afazer"),
            ("Em Progresso", "progress"),
            ("Feito", "feito"),
        ]

        def find_column_by_keywords(board, keywords):
            qs = board.columns.all()
            # procura exata
            col = qs.filter(title__iexact=keywords).first()
            if col:
                return col
            # procura por palavras-chave (icontains)
            kws = [keywords]
            # normalizar algumas variações
            if keywords.lower().startswith('a') and 'fazer' in keywords.lower():
                kws = ['fazer', 'a fazer', 'to do']
            if 'progresso' in keywords.lower() or 'progress' in keywords.lower():
                kws = ['progresso', 'fazendo', 'em progresso', 'doing', 'in progress']
            if 'feito' in keywords.lower() or 'done' in keywords.lower():
                kws = ['feito', 'concluido', 'concluído', 'done']

            for k in kws:
                col = qs.filter(title__icontains=k).first()
                if col:
                    return col
            return None

        kanban_columns = []
        for display_name, key in desired:
            col = find_column_by_keywords(board, display_name)
            cards = col.cards.all() if col else []
            kanban_columns.append({
                'key': key,
                'display_name': display_name,
                'column': col,
                'cards': cards,
            })

        ctx['kanban_columns'] = kanban_columns
        return ctx

def create_board(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        if title:
            board = Board.objects.create(title=title, description=description)
            # Criar colunas padrão para padronizar novos quadros (A Fazer, Fazendo, Feito)
            default_columns = ["A Fazer", "Fazendo", "Feito"]
            for idx, col_title in enumerate(default_columns):
                Column.objects.create(board=board, title=col_title, position=idx)
            messages.success(request, "Quadro criado com sucesso.")
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
            messages.success(request, "Coluna criada com sucesso.")
    return redirect("boards:detail", pk=board.pk)

def update_board(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == "POST":
        board.title = request.POST.get("title")
        board.description = request.POST.get("description")
        board.save()
        messages.success(request, "Quadro atualizado.")
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
        messages.success(request, "Cartão atualizado.")
    return redirect("boards:detail", pk=card.column.board.id)


def create_card(request, column_id):
    column = get_object_or_404(Column, id=column_id)
    if request.method == "POST":
        Card.objects.create(
            column=column,
            title=request.POST.get("title"),
            description=request.POST.get("description")
        )
        messages.success(request, "Cartão criado.")
    return redirect("boards:detail", pk=column.board.id)


@require_POST
def delete_card(request, card_pk):
    """Exclui um cartão e redireciona para o quadro pai."""
    card = get_object_or_404(Card, pk=card_pk)
    board_id = card.column.board.id
    card.delete()
    messages.success(request, "Cartão excluído.")
    return redirect("boards:detail", pk=board_id)


@require_POST
def delete_board(request, pk):
    """Exclui um quadro e redireciona para a lista de quadros."""
    board = get_object_or_404(Board, pk=pk)
    board.delete()
    messages.success(request, "Quadro excluído.")
    return redirect("boards:list")


@require_POST
def reorder_cards(request):
    """Recebe um JSON com a nova ordem dos cartões por coluna e atualiza DB.

    Formato esperado (JSON):
    {"columns": [{"id": 1, "cards": [3,5,2]}, {"id":2, "cards": [4,1]}]}
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"ok": False, "error": "invalid_json"}, status=400)

    columns = payload.get("columns")
    if not isinstance(columns, list):
        return JsonResponse({"ok": False, "error": "missing_columns"}, status=400)

    # Atualiza posições dentro de uma transação
    with transaction.atomic():
        for col in columns:
            col_id = col.get("id")
            cards = col.get("cards") or []
            for pos, card_id in enumerate(cards):
                try:
                    card = Card.objects.select_for_update().get(id=card_id)
                    # atualiza coluna se necessário
                    if card.column_id != col_id:
                        card.column_id = col_id
                    card.position = pos
                    card.save()
                except Card.DoesNotExist:
                    continue

    return JsonResponse({"ok": True})

