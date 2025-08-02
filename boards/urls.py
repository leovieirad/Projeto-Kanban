from django.urls import path
from .views import (
    BoardListView,
    BoardDetailView,
    create_board,
    create_column,
    create_card,
)

app_name = "boards"

urlpatterns = [
    path("", BoardListView.as_view(), name="list"),
    path("boards/novo/", create_board, name="create_board"),
    path("boards/<int:pk>/", BoardDetailView.as_view(), name="detail"),
    path("boards/<int:board_pk>/colunas/novo/", create_column, name="create_column"),
    path("colunas/<int:column_pk>/cartoes/novo/", create_card, name="create_card"),
]
