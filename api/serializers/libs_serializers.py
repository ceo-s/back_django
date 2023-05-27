from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

# Libs Serializers
from libs.models import Sport, MuscleGroup, Exercise, Product, Supplement


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
        # fields = ["id", "name", "slug", "description", "image"]
        # lookup_field = 'slug'


class FoodSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = "__all__"


class SupplementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplement
        fields = "__all__"
