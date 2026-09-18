from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.players_list, name="players_list"),
    path("player/<int:pk>/", views.player_detail, name="player_detail"),
]
