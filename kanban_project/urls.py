"""
Configuração de URLs para o projeto kanban_project.

A lista `urlpatterns` mapeia URLs para views. Para mais informações, veja:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Exemplos:
Views baseadas em função
    1. Adicione um import:  from my_app import views
    2. Adicione uma URL ao urlpatterns:  path('', views.home, name='home')
Views baseadas em classe
    1. Adicione um import:  from other_app.views import Home
    2. Adicione uma URL ao urlpatterns:  path('', Home.as_view(), name='home')
Incluindo outro arquivo de URLs
    1. Importe a função include(): from django.urls import include, path
    2. Adicione uma URL ao urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("boards.urls")),  # delegando a raiz para o app boards
]
