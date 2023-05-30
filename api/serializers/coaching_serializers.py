from rest_framework import serializers
# from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

# Coaching serializers
from coaching.models import Client, ClientStatsActive, ClientStatsArchieved, ClientBaseExercises
from coaching.models import TrainingProgram, TrainingDay, ExerciseAmount

from api.serializers import BulkUpdateOrCreateListSerializer


class ClientSerializerList(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = "__all__"
        fields = ["id", "name", "telegram", "description"]


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = "__all__"
        # list_serializer_class = ClientSerializerList


class ClientStatsActiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientStatsActive
        fields = "__all__"


class ClientStatsArchievedSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientStatsArchieved
        fields = "__all__"


class ClientBaseExercisesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientBaseExercises
        fields = "__all__"


class TrainingProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainingProgram
        fields = "__all__"


class TrainingDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainingDay
        fields = "__all__"


class ExerciseAmountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ExerciseAmount
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer


class DetailTrainingDaySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    exercises = serializers.SerializerMethodField()

    class Meta:
        model = TrainingDay
        fields = '__all__'
        list_serializer_class = BulkUpdateOrCreateListSerializer

    def get_exercises(self, obj):
        exercises = obj.examount.order_by("count")
        serializer = ExerciseAmountSerializer(exercises, many=True)
        return serializer.data


class DetailTrainingProgramSerializer(serializers.ModelSerializer):
    days = serializers.SerializerMethodField()

    class Meta:
        model = TrainingProgram
        fields = '__all__'
        list_serializer_class = BulkUpdateOrCreateListSerializer

    def get_days(self, obj):
        days = obj.days.order_by("date").prefetch_related("examount")
        serializer = DetailTrainingDaySerializer(days, many=True)
        return serializer.data
