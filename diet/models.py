from django.db import models

# Create your models here.


class DietProgram(models.Model):
    """
    Client diet program.
    """
    name = models.CharField(max_length=255)
    coach = models.ForeignKey(
        to="cabinet.TgUser", on_delete=models.CASCADE)
    client = models.ForeignKey(to="coaching.Client", on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    date_start = models.DateField(null=True)
    date_finish = models.DateField(null=True)
    recommended_products = models.ManyToManyField(
        to="libs.Product", related_name="recommended")
    forbidden_products = models.ManyToManyField(
        to="libs.Product", related_name="forbidden")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Диета"
        verbose_name_plural = "Диета"


class DayNutrients(models.Model):
    """
    Amount of daily nutrients to consume.
    """
    diet_program = models.ForeignKey(
        to="DietProgram", on_delete=models.CASCADE, related_name="nutrients")
    name = models.CharField(max_length=255)
    water = models.FloatField()
    proteins = models.FloatField()
    fats = models.FloatField()
    carbohydrates = models.FloatField()
    calories = models.FloatField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Дневной калораж / БЖУ"
        verbose_name_plural = "Дневной калораж / БЖУ"


class DietSchedule(models.Model):
    """
    Schedule of Nurtrients. Aka carb/nutrients cycling.
    """
    count = models.IntegerField()
    program = models.ForeignKey(
        to="DietProgram", on_delete=models.CASCADE, related_name="schedule")
    day_type = models.ForeignKey(to="DayNutrients", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.count)
        # return f"{self.count} of program {self.program}"

    class Meta:
        verbose_name = "Дни цикла диеты"
        verbose_name_plural = "Дни циклов диеты"


class FoodAmount(models.Model):
    """
    Product configurationn for diet day reference.
    """
    product = models.ForeignKey(to="libs.Product", on_delete=models.CASCADE)
    meal = models.ForeignKey(
        to="Meal", on_delete=models.CASCADE, related_name="foodamount")
    grams = models.FloatField(default=100.)

    def __str__(self) -> str:
        return f"{self.product} - {self.grams}"

    class Meta:
        verbose_name = "Запись о количестве продукта"
        verbose_name_plural = "Записи о количестве продуктов"


class CustomMealFoodAmount(models.Model):
    """
    Product configurationn for custom meal.
    """
    name = models.ForeignKey(to="libs.Product", on_delete=models.CASCADE)
    meal = models.ForeignKey(to="CustomMeal", on_delete=models.CASCADE)
    grams = models.FloatField(default=100.)

    def __str__(self) -> str:
        return f"{self.name} - {self.grams}"

    class Meta:
        verbose_name = "Запись о количестве продукта"
        verbose_name_plural = "Записи о количестве продуктов"

# TODO сделать логику для расписания приёма добавок и внесения записей с дозировками


class SupplementAmount(models.Model):
    """
    Supplement configurationn for diet day reference.
    """
    name = models.ForeignKey(to="libs.Supplement", on_delete=models.CASCADE)
    program = models.ForeignKey(
        to="DietProgram", on_delete=models.CASCADE)
    milligrams = models.FloatField(default=1000.)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "Запись о количестве БАДа"
        verbose_name_plural = "Записи о количестве БАДов"


class Meal(models.Model):
    """
    Meal on diet day.
    """
    name = models.CharField(max_length=127)
    day = models.ForeignKey(to="DietProgramDay",
                            on_delete=models.CASCADE, related_name="meals")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Приём пищи"
        verbose_name_plural = "Приёмы пищи"


class CustomMeal(models.Model):
    """
    Custom meal of diet day.
    """
    name = models.CharField(max_length=127)
    coach = models.ForeignKey(
        to="cabinet.TgUser", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Кастомный приём пищи"
        verbose_name_plural = "Кастомные приёмы пищи"


class DietProgramDay(models.Model):
    """
    Reference diet day for program.
    """
    name = models.CharField(max_length=127)
    diet_program = models.ForeignKey(
        to="DietProgram", on_delete=models.CASCADE, related_name="day_reference")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Рацион на день"
        verbose_name_plural = "Рационы на день"
