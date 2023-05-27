from django.contrib import admin
from . import models

# Register your models here.

admin.site.register([
    models.MuscleGroup,
    models.Exercise,
    models.Product,
    models.Supplement,
])
