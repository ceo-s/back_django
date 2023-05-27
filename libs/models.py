from django.db import models
from .services.service import custom_exercise_path, path_post_pic
from django.utils.text import slugify

# Create your models here.


class Sport(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Спорт"
        verbose_name_plural = "Спорт"


class MuscleGroup(models.Model):
    name = models.CharField(max_length=250)
    functions = models.TextField()
    description = models.TextField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Группа мышц"
        verbose_name_plural = "Группы мышц"


class Exercise(models.Model):
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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Exercise, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Упражнение"
        verbose_name_plural = "Упражнения"


class Product(models.Model):
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
    name = models.CharField(max_length=127)
    daily_value = models.FloatField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "БАД"
        verbose_name_plural = "БАДы"


# TODO Я не уверен нужен ли вообще артикл, но пост надо бы перенести в cabinet который будет
# переименован и объединён с cabinet. Его надо назвать попонятняй он будет типо блока для конструктора
# личного кабинета

# class Article(models.Model):
#     user = models.ForeignKey(to="cabinet.TgUser", null=True, blank=True, on_delete=models.CASCADE)
#     source = models.CharField(max_length=255, null=True, blank=True)
#     source_link = models.TextField(null=True, blank=True)
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     sport = models.ManyToManyField(to="cabinet.Sport", default='cabinet.Sport.objects.get_current', blank=True)
#     date_creation = models.DateTimeField(auto_now_add=True)
#     date_update = models.DateTimeField(auto_now=True)

#     def __str__(self) -> str:
#         return self.title

#     class Meta:
#         verbose_name = "Статья"
#         verbose_name_plural = "Статьи"
