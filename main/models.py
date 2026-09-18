from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def validate_not_in_future(value):
    if value and value > date.today():
        raise ValidationError("Дата рождения не может быть в будущем.")


class Player(models.Model):
    class Position(models.TextChoices):
        GOALKEEPER = "GK", "Вратарь"
        DEFENDER = "DF", "Защитник"
        MIDFIELDER = "MF", "Полузащитник"
        FORWARD = "FW", "Нападающий"

    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    jersey_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        verbose_name="Игровой номер",
    )
    position = models.CharField(max_length=2, choices=Position.choices, verbose_name="Позиция")
    club = models.CharField(max_length=100, verbose_name="Клуб")
    photo = models.ImageField(
        upload_to="players/", blank=True, null=True, verbose_name="Фотография"
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        validators=[validate_not_in_future],
        verbose_name="Дата рождения",
    )
    nationality = models.CharField(max_length=100, blank=True, verbose_name="Гражданство")
    height_cm = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(100), MaxValueValidator(250)],
        verbose_name="Рост (см)",
    )
    weight_kg = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(30), MaxValueValidator(250)],
        verbose_name="Вес (кг)",
    )
    appearances = models.PositiveIntegerField(default=0, verbose_name="Матчи")
    goals = models.PositiveIntegerField(default=0, verbose_name="Голы")
    assists = models.PositiveIntegerField(default=0, verbose_name="Голевые передачи")

    class Meta:
        ordering = ("club", "jersey_number", "last_name", "first_name")
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"
        constraints = [
            models.UniqueConstraint(
                fields=("club", "jersey_number"),
                name="unique_jersey_number_per_club",
            )
        ]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"#{self.jersey_number} {self.full_name} ({self.club})"
