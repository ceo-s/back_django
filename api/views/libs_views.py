from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from libs.models import Exercise
from api.serializers import libs_serializers
from libs.models import Sport, MuscleGroup, Exercise, Product, Supplement, ExerciseMedia
from .. import mixins

# Libs API Views


class SportViewSet(ModelViewSet):
    queryset = Sport.objects.all()
    serializer_class = libs_serializers.SportSerializer


class MuscleGroupViewSet(ModelViewSet):
    queryset = MuscleGroup.objects.all()
    serializer_class = libs_serializers.MuscleGroupSerializer


class ExerciseViewSet(mixins.FilteredSearch, ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = libs_serializers.ExerciseSerializer

    def retrieve(self, request: Request, pk=None, *args, **kwargs):

        instance = self.get_queryset().get(id=pk)
        serializer = libs_serializers.ExtendedExerciseSerializer(
            instance=instance, context={"request": request})
        response = serializer.data
        response["media"] = libs_serializers.ExerciseMediaSerializer(
            instance=instance.exercise_media.all(), many=True, context={"request": request}).data
        return Response(response)


class ExerciseMediaViewSet(mixins.FilteredSearch, ModelViewSet):
    queryset = ExerciseMedia.objects.all()
    serializer_class = libs_serializers.ExerciseMediaSerializer


class FoodViewSet(mixins.FilteredSearch, ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = libs_serializers.FoodSerializer


class SupplementViewSet(mixins.FilteredSearch, ModelViewSet):
    queryset = Supplement.objects.all()
    serializer_class = libs_serializers.SupplementSerializer
