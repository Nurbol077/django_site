from django.shortcuts import get_object_or_404, render

from .models import Player


def players_list(request):
    players = Player.objects.all()
    selected_position = request.GET.get("position", "")
    valid_positions = {value for value, _ in Player.Position.choices}

    if selected_position in valid_positions:
        players = players.filter(position=selected_position)
    else:
        selected_position = ""

    return render(
        request,
        "players.html",
        {
            "players": players,
            "positions": Player.Position.choices,
            "selected_position": selected_position,
        },
    )


def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    return render(request, "player_detail.html", {"player": player})
