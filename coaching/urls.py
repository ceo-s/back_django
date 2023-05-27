from django.urls import path
from . import views

urlpatterns = [
    path('programs/', views.TrainingProgramsView.as_view(), name="programs"),
    path('program/', views.TrainingProgramView.as_view(), name="program"),
    path('clients/', views.ClientsListView.as_view(), name="clients"),
]