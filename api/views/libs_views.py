from rest_framework.viewsets import ModelViewSet
from libs.models import Exercise
from api.serializers import libs_serializers
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
