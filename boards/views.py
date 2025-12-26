from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("boards:login")
        return super().dispatch(request, *args, **kwargs)
    
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
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("boards:login")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """Renderiza TODAS as colunas do quadro.

        - Mantém cores específicas para A Fazer / Em Progresso / Feito
        - Para demais colunas, atribui uma classe de cor determinística com base no id
        """
        ctx = super().get_context_data(**kwargs)
        board = self.get_object()

        def classify_column(col):
            name = (col.title or "").lower()
            # padrões conhecidos
            if ('fazer' in name) or (name.strip() in ['to do', 'a fazer']):
                return 'afazer', 'col-afazer'
            if ('progresso' in name) or ('fazendo' in name) or ('doing' in name) or ('in progress' in name):
                return 'progress', 'col-progress'
            if ('feito' in name) or ('conclu' in name) or (name.strip() == 'done'):
                return 'feito', 'col-feito'
            # demais colunas: mapeia para paleta 1..8 de forma determinística
            color_idx = (col.id % 8) + 1
            return f'col-{col.id}', f'col-color-{color_idx}'

        kanban_columns = []
        for col in board.columns.all():
            key, class_name = classify_column(col)
            # Nome amigável padronizado para as colunas principais
            if class_name == 'col-afazer':
                display_name = 'A Fazer'
            elif class_name == 'col-progress':
                display_name = 'Em Progresso'
            elif class_name == 'col-feito':
                display_name = 'Feito'
            else:
                display_name = col.title

            kanban_columns.append({
                'key': key,
                'class_name': class_name,
                'display_name': display_name,
                'column': col,
                'cards': col.cards.all(),
            })

        ctx['kanban_columns'] = kanban_columns
        return ctx

def create_board(request):
    """Cria um novo quadro."""
    if not request.user.is_authenticated:
        return redirect("boards:login")
    
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        if title:
            board = Board.objects.create(title=title, description=description)
            # Criar colunas padrão para padronizar novos quadros (A Fazer, Fazendo, Feito)
            default_columns = ["A Fazer", "Em Progresso", "Feito"]
            for idx, col_title in enumerate(default_columns):
                Column.objects.create(board=board, title=col_title, position=idx)
            messages.success(request, "Quadro criado com sucesso.")
            return redirect("boards:detail", pk=board.pk)
    return render(request, "boards/board_form.html")

def create_column(request, board_pk):
    """Cria uma nova coluna em um quadro."""
    if not request.user.is_authenticated:
        return redirect("boards:login")
    
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
    """Atualiza informações de um quadro."""
    if not request.user.is_authenticated:
        return redirect("boards:login")
    
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
    """Marca um cartão como feito ou não."""
    if not request.user.is_authenticated:
        return redirect("boards:login")
    
    card = get_object_or_404(Card, pk=card_pk)
    card.is_done = not card.is_done
    card.save()
    return JsonResponse({"is_done": card.is_done})

def edit_card(request, card_id):
    """Edita um cartão."""
    if not request.user.is_authenticated:
        return redirect("boards:login")
    
    card = get_object_or_404(Card, id=card_id)
    if request.method == "POST":
        card.title = request.POST.get("title")
        card.description = request.POST.get("description")
        card.priority = request.POST.get("priority", "medium")
        card.save()
        messages.success(request, "Cartão atualizado.")
    return redirect("boards:detail", pk=card.column.board.id)


def create_card(request, column_id):
    """Cria um novo cartão em uma coluna."""
    if not request.user.is_authenticated:
        return redirect("boards:login")
    
    column = get_object_or_404(Column, id=column_id)
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if not title:
            messages.error(request, "O título do cartão é obrigatório.")
        else:
            Card.objects.create(
                column=column,
                title=title,
                description=request.POST.get("description", "").strip(),
                priority=request.POST.get("priority", "medium")
            )
            messages.success(request, "Cartão criado.")
    return redirect("boards:detail", pk=column.board.id)


@require_POST
def delete_card(request, card_pk):
    """Exclui um cartão e redireciona para o quadro pai."""
    if not request.user.is_authenticated:
        return redirect("boards:login")
    
    card = get_object_or_404(Card, pk=card_pk)
    board_id = card.column.board.id
    card.delete()
    messages.success(request, "Cartão excluído.")
    
    # Se for AJAX, retorna JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({"ok": True, "board_id": board_id})
    
    return redirect("boards:detail", pk=board_id)


@require_POST
def delete_column(request, column_pk):
    """Exclui uma coluna e retorna para o quadro pai."""
    if not request.user.is_authenticated:
        return JsonResponse({"ok": False, "error": "unauthorized"}, status=401)
    
    column = get_object_or_404(Column, pk=column_pk)
    board_id = column.board.id
    board = column.board
    
    # Verificar se há apenas uma coluna
    if board.columns.count() <= 1:
        return JsonResponse({"ok": False, "error": "Não é possível deletar a última coluna"}, status=400)
    
    column.delete()
    
    # Se for AJAX, retorna JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({"ok": True, "board_id": board_id})
    
    return redirect("boards:detail", pk=board_id)


@require_POST
def delete_board(request, pk):
    """Exclui um quadro e redireciona para a lista de quadros."""
    if not request.user.is_authenticated:
        return redirect("boards:login")
    
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
    if not request.user.is_authenticated:
        return JsonResponse({"ok": False, "error": "unauthorized"}, status=401)
    
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


@require_POST
def reorder_columns(request):
    """Recebe um JSON com a nova ordem das colunas e atualiza DB.

    Formato esperado (JSON):
    {"columns": [1, 3, 2]}  # IDs das colunas em nova ordem
    """
    if not request.user.is_authenticated:
        return JsonResponse({"ok": False, "error": "unauthorized"}, status=401)
    
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"ok": False, "error": "invalid_json"}, status=400)

    columns_order = payload.get("columns")
    if not isinstance(columns_order, list):
        return JsonResponse({"ok": False, "error": "missing_columns"}, status=400)

    # Atualiza posições das colunas dentro de uma transação
    with transaction.atomic():
        for pos, col_id in enumerate(columns_order):
            try:
                column = Column.objects.select_for_update().get(id=col_id)
                column.position = pos
                column.save()
            except Column.DoesNotExist:
                continue

    return JsonResponse({"ok": True})


# ============== VIEWS DE AUTENTICAÇÃO ==============

def login_view(request):
    """View para login de usuários."""
    if request.user.is_authenticated:
        return redirect("boards:list")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Bem-vindo, {user.first_name or user.username}!")
            return redirect("boards:list")
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    
    return render(request, "boards/login.html")


def register_view(request):
    """View para cadastro de novos usuários."""
    if request.user.is_authenticated:
        return redirect("boards:list")
    
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")
        
        # Validações
        if not username or not email or not password:
            messages.error(request, "Todos os campos são obrigatórios.")
            return render(request, "boards/register.html")
        
        if len(password) < 6:
            messages.error(request, "A senha deve ter no mínimo 6 caracteres.")
            return render(request, "boards/register.html")
        
        if password != password_confirm:
            messages.error(request, "As senhas não conferem.")
            return render(request, "boards/register.html")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Este usuário já existe.")
            return render(request, "boards/register.html")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Este email já está cadastrado.")
            return render(request, "boards/register.html")
        
        # Criar usuário
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            password=password
        )
        
        messages.success(request, "Conta criada com sucesso! Faça login para continuar.")
        return redirect("boards:login")
    
    return render(request, "boards/register.html")


def logout_view(request):
    """View para logout de usuários."""
    logout(request)
    messages.success(request, "Você saiu com sucesso.")
    return redirect("boards:login")


@login_required
def profile_view(request):
    """Tela de perfil para editar informações básicas do usuário atual."""
    user = request.user

    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()

        # Atualiza somente campos permitidos
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        messages.success(request, "Perfil atualizado com sucesso.")
        return redirect("boards:profile")

    return render(request, "boards/profile.html", {"user_obj": user})


@login_required
def change_password_view(request):
    """Altera a senha do usuário autenticado usando PasswordChangeForm."""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # mantém sessão ativa
            messages.success(request, "Senha alterada com sucesso.")
        else:
            # Coletar mensagens de erro do formulário (sem prefixo do nome do campo)
            errors = []
            for _field, field_errors in form.errors.items():
                for err in field_errors:
                    errors.append(str(err))
            if errors:
                messages.error(request, "\n".join(errors))
            else:
                messages.error(request, "Não foi possível alterar a senha.")
        return redirect("boards:profile")
    # Em GET apenas redireciona para o perfil
    return redirect("boards:profile")

