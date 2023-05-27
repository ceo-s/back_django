from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.DietSchedule)
class DietScheduleAdmin(admin.ModelAdmin):
    list_per_page = 900


@admin.register(models.DayNutrients,)
class DayNutrientsAdmin(admin.ModelAdmin):
    list_per_page = 900


admin.site.register([
    # models.DayNutrients,
    # models.DietSchedule,
    models.DietProgram,
    models.FoodAmount,
    models.SupplementAmount,
    models.Meal,
    models.CustomMeal,
    models.DietProgramDay,
])
