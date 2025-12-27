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
    login_view,
    register_view,
    logout_view,
    profile_view,
    change_password_view,
)

app_name = "boards"

urlpatterns = [
    # Autenticação
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("profile/password/", change_password_view, name="change_password"),
    
    # Quadros
    path("", BoardListView.as_view(), name="list"),
    path("boards/novo/", create_board, name="create_board"),
    path("boards/<int:pk>/", BoardDetailView.as_view(), name="detail"),
    path("boards/<int:board_pk>/colunas/novo/", create_column, name="create_column"),
    
    # ✔️ manter só esta rota de criar cartão
    path("colunas/<int:column_id>/cartoes/novo/", create_card, name="create_card"),

    path("boards/<int:pk>/editar/", update_board, name="update_board"),
    path("cartoes/<int:card_pk>/toggle-done/", toggle_card_done, name="toggle_card_done"),

    path("card/<int:card_id>/edit/", views.edit_card, name="edit_card"),
    path("cartoes/<int:card_pk>/delete/", views.delete_card, name="delete_card"),
    path("colunas/<int:column_pk>/delete/", views.delete_column, name="delete_column"),
    path("boards/<int:pk>/delete/", views.delete_board, name="delete_board"),
    path("api/cards/reorder/", views.reorder_cards, name="reorder_cards"),
    path("api/columns/reorder/", views.reorder_columns, name="reorder_columns"),
    
    # Comentários
    path("card/<int:card_id>/comments/", views.get_card_comments, name="get_card_comments"),
    path("card/<int:card_id>/comments/add/", views.add_card_comment, name="add_card_comment"),
    path("comments/<int:comment_id>/delete/", views.delete_card_comment, name="delete_card_comment"),
]
