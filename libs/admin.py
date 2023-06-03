from django.contrib import admin
from . import models

# Register your models here.

admin.site.register([
    models.MuscleGroup,
    models.Exercise,
    models.ExerciseMedia,
    models.Product,
    models.Supplement,
])
