from django.db import models
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
    media = models.FileField(default="media/")
    muscle = models.ManyToManyField(to="MuscleGroup")
    # TODO переименовать в спорт
    sport_tag = models.ManyToManyField(to="Sport")
    user = models.ForeignKey(
        to="cabinet.TgUser", on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Упражнение"
        verbose_name_plural = "Упражнения"


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
