from django.forms import model_to_dict
from django.http import QueryDict
from rest_framework import status
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from libs.models import Exercise
from api.serializers import libs_serializers
from utils.services import date_time_fuctions
from .. import mixins

# Libs API Views

from libs.models import Sport, MuscleGroup, Exercise, Product, Supplement


class SportViewSet(ModelViewSet):
    queryset = Sport.objects.all()
    serializer_class = libs_serializers.SportSerializer


class MuscleGroupViewSet(ModelViewSet):
    queryset = MuscleGroup.objects.all()
    serializer_class = libs_serializers.MuscleGroupSerializer


class ExerciseViewSet(mixins.FilteredSearch, ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = libs_serializers.ExerciseSerializer


class FoodViewSet(mixins.FilteredSearch, ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = libs_serializers.FoodSerializer


class SupplementViewSet(mixins.FilteredSearch, ModelViewSet):
    queryset = Supplement.objects.all()
    serializer_class = libs_serializers.SupplementSerializer
