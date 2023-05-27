from django.shortcuts import render
from django.views.generic import ListView, View, DetailView, UpdateView

from . import models
# Create your views here.

class TrainingProgramsView(ListView):
    model = models.TrainingProgram
    template_name = 'coaching/programs.html'

class TrainingProgramView(View):
    def get(self, request, *args, **kwargs):
        return render(request=request, template_name='coaching/program.html')
    

class ClientsListView(ListView):
    model = models.Client
    template_name = 'coaching/clients.html'
