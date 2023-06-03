from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

# Libs Serializers
from libs.models import Sport, MuscleGroup, Exercise, ExerciseMedia, Product, Supplement


class SportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sport
        fields = "__all__"


class MuscleGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = MuscleGroup
        fields = "__all__"


class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = "__all__"


class ExtendedExerciseSerializer(serializers.ModelSerializer):
    # media = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = "__all__"

    # def get_media(self, obj):
    #     # queryset = obj.exercise_media.values_list("file", flat=True)
    #     queryset = [media.file.url for media in obj.exercise_media.all()]
    #     queryset = obj.exercise_media.all()
    #     serializer = ExerciseMediaSerializer(
    #         queryset, many=True)
    #     return serializer.data
    #     # return queryset


class ExerciseMediaSerializer(serializers.ModelSerializer):
    # file = serializers.FileField(use_url=True)

    class Meta:
        model = ExerciseMedia
        fields = ("id", "file", "type")


class FoodSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = "__all__"


class SupplementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplement
        fields = "__all__"
