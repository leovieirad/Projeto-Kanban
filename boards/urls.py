from django.urls import path
from . import views
from .views import (
    BoardListView,
    BoardDetailView,
    create_board,
    create_column,
    create_card,
    update_board,
    toggle_card_done,
)

app_name = "boards"

urlpatterns = [
    path("", BoardListView.as_view(), name="list"),
    path("boards/novo/", create_board, name="create_board"),
    path("boards/<int:pk>/", BoardDetailView.as_view(), name="detail"),
    path("boards/<int:board_pk>/colunas/novo/", create_column, name="create_column"),
    
    # ✔️ manter só esta rota de criar cartão
    path("colunas/<int:column_pk>/cartoes/novo/", create_card, name="create_card"),

    path("boards/<int:pk>/editar/", update_board, name="update_board"),
    path("cartoes/<int:card_pk>/toggle-done/", toggle_card_done, name="toggle_card_done"),

    path("card/<int:card_id>/edit/", views.edit_card, name="edit_card"),
]
