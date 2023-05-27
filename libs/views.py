from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . import models

# Create your views here.

class ExercisesListView(ListView):
    model = models.Exercise
    template_name = "libs/exercises.html"


class ExerciseDetailView(DetailView):
    model = models.Exercise
    template_name = "libs/exercise.html"
    