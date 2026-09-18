from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Player


class PlayerModelTests(TestCase):
    def setUp(self):
        self.player = Player.objects.create(
            first_name="Иван",
            last_name="Иванов",
            jersey_number=10,
            position=Player.Position.FORWARD,
            club="Тест",
            appearances=12,
            goals=5,
            assists=3,
        )

    def test_string_representation_and_full_name(self):
        self.assertEqual(self.player.full_name, "Иван Иванов")
        self.assertEqual(str(self.player), "#10 Иван Иванов (Тест)")

    def test_jersey_number_is_unique_within_a_club(self):
        duplicate = Player(
            first_name="Пётр",
            last_name="Петров",
            jersey_number=10,
            position=Player.Position.DEFENDER,
            club="Тест",
        )

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_profile_values_are_validated(self):
        invalid = Player(
            first_name="Анна",
            last_name="Смирнова",
            jersey_number=100,
            position=Player.Position.GOALKEEPER,
            club="Тест",
            height_cm=99,
            birth_date=date.today() + timedelta(days=1),
        )

        with self.assertRaises(ValidationError):
            invalid.full_clean()


class PlayerViewsTests(TestCase):
    def setUp(self):
        self.forward = Player.objects.create(
            first_name="Иван",
            last_name="Иванов",
            jersey_number=9,
            position=Player.Position.FORWARD,
            club="Тест",
        )
        Player.objects.create(
            first_name="Пётр",
            last_name="Петров",
            jersey_number=1,
            position=Player.Position.GOALKEEPER,
            club="Тест",
        )

    def test_catalog_filters_by_position(self):
        response = self.client.get(reverse("main:players_list"), {"position": "FW"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Иван Иванов")
        self.assertNotContains(response, "Пётр Петров")

    def test_player_profile_is_available(self):
        response = self.client.get(reverse("main:player_detail", args=[self.forward.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Иван Иванов")
        self.assertContains(response, "#9")

    def test_missing_player_returns_404(self):
        response = self.client.get(reverse("main:player_detail", args=[999]))

        self.assertEqual(response.status_code, 404)
