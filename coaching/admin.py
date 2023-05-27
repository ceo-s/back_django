from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.ClientBaseExercises)
class BaseExAdmin(admin.ModelAdmin):
    filter_horizontal = ("exercises",)


admin.site.register([
    models.Client,
    models.ClientStatsActive,
    models.ClientStatsArchieved,
    # models.ClientBaseExercises ,
    models.TrainingProgram,
    models.TrainingDay,
    models.ExerciseAmount,
])
