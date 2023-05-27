from django.dispatch import receiver
from django.db.models.signals import post_save
from typing import Iterable, Optional
from django.db import models
import json
import datetime
from django.utils.timezone import now
from django.apps import apps
from .services.defaults import default_program
from utils.services import date_time_fuctions

# Create your models here.


class Client(models.Model):
    name = models.CharField(max_length=127)
    telegram = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    sport = models.ManyToManyField(to="libs.Sport", blank=True)
    coach = models.ForeignKey(
        to="cabinet.TgUser", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class ClientStats(models.Model):
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    bodyfat_percent = models.FloatField(null=True, blank=True)
    neck = models.FloatField(null=True, blank=True)
    shoulders = models.FloatField(null=True, blank=True)
    chest = models.FloatField(null=True, blank=True)
    bicep = models.FloatField(null=True, blank=True)
    forearm = models.FloatField(null=True, blank=True)
    waist = models.FloatField(null=True, blank=True)
    glutes = models.FloatField(null=True, blank=True)
    legs = models.FloatField(null=True, blank=True)
    calves = models.FloatField(null=True, blank=True)

    class Meta:
        abstract = True


class ClientStatsActive(ClientStats):
    client = models.OneToOneField(
        to="Client", on_delete=models.CASCADE, primary_key=True)
    date_update = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"Stats of {self.client.name}"

    class Meta:
        verbose_name = "Статистика клиента"
        verbose_name_plural = "Статистика клиентов"


class ClientStatsArchieved(ClientStats):
    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    date_created = models.DateField()
    date_archieved = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Archieved stats of {self.client}"

    class Meta:
        verbose_name = "Архивная статистика клиента"
        verbose_name_plural = "Архивная статистика клиентов"


class ClientBaseExercises(models.Model):
    client = models.OneToOneField(
        "Client", on_delete=models.CASCADE)
    exercises = models.ManyToManyField(to='libs.Exercise')

    def __str__(self) -> str:
        return f"Base exercises of {self.client}"

    class Meta:
        verbose_name = "Упражнения для отслеживания статистики"
        verbose_name_plural = "Упражнения для отслеживания статистики"


class TrainingProgram(models.Model):
    coach = models.ForeignKey(
        to="cabinet.TgUser", on_delete=models.CASCADE)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=127, default="Новая программа")
    description = models.TextField()
    time_start = models.DateField()
    time_finish = models.DateField()

    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        self.time_start = date_time_fuctions.weekstart_date(self.time_start)
        self.time_finish = date_time_fuctions.weekend_date(self.time_finish)
        super().save()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Программа тренировок"
        verbose_name_plural = "Программы тренировок"


class TrainingDay(models.Model):
    program = models.ForeignKey(
        to="TrainingProgram", on_delete=models.CASCADE, related_name="days")
    date = models.DateField()

    def __str__(self) -> str:
        return f"{self.date}"

    class Meta:
        verbose_name = "Тренироваочный день"
        verbose_name_plural = "Тренировочные дни"


class ExerciseAmount(models.Model):
    exercise = models.ForeignKey(
        to="libs.Exercise", on_delete=models.CASCADE, null=True)
    name = models.CharField(blank=True)
    count = models.IntegerField()
    reps = models.IntegerField(null=True)
    sets = models.IntegerField(null=True)
    weight = models.FloatField(null=True)
    comment = models.TextField(blank=True)
    training_day = models.ForeignKey(
        to="TrainingDay", on_delete=models.CASCADE, related_name="examount")

    class Meta:
        verbose_name = "Запись об упражнениях"
        verbose_name_plural = "Записи об упражнениях"


@receiver(post_save, sender=Client)
def on_client_creation(sender, instance, **kwargs):
    """При добавлении новго клиента:
       - создаёт ClientStatsActive instanse
       - создаёт ClientBaseExercises instance."""
    if kwargs['created']:
        ClientStatsActive.objects.create(client=instance)
        ClientBaseExercises.objects.create(
            client=instance)
        # FIXME
        # exercises = apps.get_model('libs', 'Exercise').get_base_exercises()
        # client_base_exercises.exercises.add(*exercises)


@receiver(post_save, sender=TrainingProgram)
def fill_program(sender, instance, **kwargs):
    if kwargs['created']:
        days = date_time_fuctions.get_interval_dates(
            str(instance.time_start), str(instance.time_finish))
        training_days = [TrainingDay(program=instance, date=day)
                         for day in days]
        TrainingDay.objects.bulk_create(training_days)


"""
height: 100.21
weight: 100.21
bodyfat_percent: 100.21
neck: 100.21
shoulders: 100.21
chest: 100.21
bicep: 100.21
forearm: 100.21
waist: 100.21
glutes: 100.21
legs: 100.21
calves: 100.21
date_update: 100.21

"""
