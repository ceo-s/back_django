from django.db import models
from utils.services.model_services import PathGenerator
from .services.service import custom_exercise_path
# Create your models here.


class Sport(models.Model):
    """
    Sport card.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Спорт"
        verbose_name_plural = "Спорт"


class MuscleGroup(models.Model):
    """
    Muscle group card.
    """
    name = models.CharField(max_length=250)
    functions = models.TextField()
    description = models.TextField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Группа мышц"
        verbose_name_plural = "Группы мышц"


class Exercise(models.Model):
    """
    Exrcise card.
    """
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField()
    # Null should be removed
    image = models.ImageField(
        upload_to=custom_exercise_path, null=True)
    muscle = models.ManyToManyField(to="MuscleGroup")
    # TODO переименовать в спорт
    sport = models.ManyToManyField(to="Sport")
    user = models.ForeignKey(
        to="cabinet.TgUser", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Упражнение"
        verbose_name_plural = "Упражнения"


class ExerciseMedia(models.Model):
    """
    Mediafiles for exercise.
    """
    IMAGE = "IMG"
    VIDEO = "VID"
    TYPE_CHOICES = [
        (IMAGE, "Image"),
        (VIDEO, "Video")
    ]
    exercise = models.ForeignKey(
        to="Exercise", on_delete=models.CASCADE, related_name="exercise_media")
    file = models.FileField(upload_to="exercise_media")
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)

    class Meta:
        verbose_name = "Медиа-файл упражнения"
        verbose_name_plural = "Медиа-файлы упражнений"


class Product(models.Model):
    """
    Product card.
    """
    name = models.CharField(max_length=127)
    calories = models.FloatField()
    proteins = models.FloatField()
    fats = models.FloatField()
    carbohydrates = models.FloatField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Supplement(models.Model):
    """
    Supplement card.
    """
    name = models.CharField(max_length=127)
    daily_value = models.FloatField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "БАД"
        verbose_name_plural = "БАДы"
