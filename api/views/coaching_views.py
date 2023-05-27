from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from api.serializers import coaching_serializers, diet_serializers
from utils.services import date_time_fuctions
from api.services import model_services
from .. import mixins

from diet import models as diet_models
from libs import models as libs_models
from coaching import models as coaching_models

# Coaching API Views
from coaching.models import Client, ClientStatsActive, ClientStatsArchieved, ClientBaseExercises
from coaching.models import TrainingProgram, TrainingDay, ExerciseAmount


class ClientViewSet(mixins.FilteredSearch, ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = coaching_serializers.ClientSerializer

    def list(self, request):
        queryset = self.get_queryset().filter(coach=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request: Request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.validated_data["coach"] = request.user
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data, headers=headers)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"Error": serializer.errors})

    @action(methods=["get"], detail=True, url_name="info")
    def get_all_info(self, request: Request, pk=None):
        data = model_services.get_client_info(pk)
        return Response(status=status.HTTP_200_OK, data=data)


class ClientStatsActiveViewSet(ModelViewSet):
    queryset = ClientStatsActive.objects.all()
    serializer_class = coaching_serializers.ClientStatsActiveSerializer


class ClientStatsArchievedViewSet(ModelViewSet):
    queryset = ClientStatsArchieved.objects.all()
    serializer_class = coaching_serializers.ClientStatsArchievedSerializer


class ClientBaseExercisesViewSet(ModelViewSet):
    queryset = ClientBaseExercises.objects.all()
    serializer_class = coaching_serializers.ClientBaseExercisesSerializer

    def retrieve(self, request: Request, pk=None):
        queryset = ClientBaseExercises.objects.get(client__id=pk)
        serializer = coaching_serializers.ClientBaseExercisesSerializer(
            queryset)
        return Response(serializer.data)


class TrainingProgramViewSet(mixins.FilteredSearch, ModelViewSet):
    queryset = TrainingProgram.objects.all()
    serializer_class = coaching_serializers.TrainingProgramSerializer

    @action(methods=["get"], detail=True, url_name="get_program")
    def get_program(self, request: Request, pk=None):
        queryset = self.get_queryset().prefetch_related("days").get(id=pk)
        serializer = coaching_serializers.DetailTrainingProgramSerializer(
            queryset)
        return Response(serializer.data)

    def create(self, request: Request, *args, **kwargs):
        data = request.data.dict()
        data["coach"] = request.user.id

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"Error": serializer.errors})

    def update(self, request: Request, pk=None, *args, **kwargs):
        instance = self.get_object()
        serializer = coaching_serializers.TrainingProgramSerializer(
            instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
        weeks = request.data.get("weeks")
        days = []

        for week in weeks:
            days += week

        _, created_days = model_services.perform_update(data=days,
                                                        serializer=coaching_serializers.DetailTrainingDaySerializer,
                                                        context={"model": coaching_models.TrainingDay,
                                                                 "fields": ("date",),
                                                                 "foreign_keys_fields": []},
                                                        many=True,
                                                        program__id=instance.id)
        exercises = []
        days_ids = []

        for day in days:
            try:
                days_ids.append(day["id"])
                exercises += day["exercises"]
            except KeyError:
                day_id = created_days.pop(0).id
                days_ids.append(day_id)
                for exercise in day["exercises"]:
                    exercise["training_day"] = day_id
                    exercises.append(exercise)

        model_services.perform_update(data=exercises,
                                      serializer=coaching_serializers.ExerciseAmountSerializer,
                                      context={"model": coaching_models.ExerciseAmount,
                                               "fields": ("name", "count", "reps", "sets", "weight", "comment", "exercise"),
                                               "foreign_keys_fields": []},
                                      many=True,
                                      training_day__id__in=days_ids)

        return Response(status=status.HTTP_202_ACCEPTED)


class TrainingDayViewSet(ModelViewSet):
    queryset = TrainingDay.objects.all()
    serializer_class = coaching_serializers.TrainingDaySerializer


class ExerciseAmountViewSet(ModelViewSet):
    queryset = ExerciseAmount.objects.all()
    serializer_class = coaching_serializers.ExerciseAmountSerializer
