from django.urls import path
from . import views

urlpatterns = [
    path('exercises/', views.ExercisesListView.as_view(), name="exercises"),
    path('exercises/<slug:slug>/', views.ExerciseDetailView.as_view(), name="exercise"),
]
