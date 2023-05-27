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
from api.serializers import diet_serializers
from utils.services import date_time_fuctions
from ..services import model_services
from .. import mixins


from diet.models import DietProgram, DayNutrients, DietSchedule, FoodAmount
from diet.models import SupplementAmount, Meal, CustomMeal, DietProgramDay


class DietProgramViewSet(mixins.FilteredSearch, ModelViewSet):
    queryset = DietProgram.objects.all()
    serializer_class = diet_serializers.DietProgramSerializer

    def create(self, request: Request, *args, **kwargs):
        # BUG приходит дикт если отпрака без csrf токена. Не уверен что из-за него но начнём с него
        data = request.data.dict()
        data["coach"] = request.user.id

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data, headers=headers)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"Error": serializer.errors})

    @action(methods=["get"], detail=True, url_name="get_program")
    def get_program(self, request: Request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()\
            .prefetch_related("forbidden_products", "recommended_products")\
            .prefetch_related("day_reference", "nutrients", "schedule")\
            .get(id=pk)
        serializer = diet_serializers.ExtendedDietProgramSerializer(
            queryset)
        headers = self.get_success_headers(serializer)
        return Response(status=status.HTTP_200_OK, data=serializer.data, headers=headers)

    def update(self, request: Request, pk=None, *args, **kwargs):
        print("SUKA", request.data)
        instance = self.get_object()
        serializer = diet_serializers.ExtendedDietProgramSerializer(
            data=request.data)
        if serializer.is_valid():
            serializer.update(instance=instance,
                              validated_data=serializer.validated_data)
        nutrients = request.data.get("nutrients")
        model_services.perform_update(data=nutrients,
                                      serializer=diet_serializers.DayNutrientsSerializer,
                                      context={"model": DayNutrients,
                                               "fields": ("name", "water", "proteins", "fats", "carbohydrates", "calories",),
                                               "foreign_keys_fields": []},
                                      many=True,
                                      diet_program__id=instance.id)
        # nutrients_serializer = diet_serializers.DayNutrientsSerializer(data=nutrients, many=True)
        # # if nutrients_serializer.is_valid(raise_exception=True):
        # #     print(nutrients_serializer.validated_data)
        schedule = request.data.get("schedule")
        model_services.perform_update(data=schedule,
                                      serializer=diet_serializers.DietScheduleSerializer,
                                      context={"model": DietSchedule,
                                               "fields": ("day_type",),
                                               "foreign_keys_fields": []},
                                      many=True,
                                      program__id=instance.id)

        day_reference = request.data.get("day_reference")
        _, created_days = model_services.perform_update(data=day_reference,
                                                        serializer=diet_serializers.DietProgramDaySerializer,
                                                        context={"model": DietProgramDay,
                                                                 "fields": ("name",),
                                                                 "foreign_keys_fields": []},
                                                        many=True,
                                                        diet_program__id=instance.id)

        meal_days_ids = []
        meals = []
        # for id, meal in {day.get("id"): day.get("meals") for day in day_reference}.items():
        #     meal_days_ids.append(id)
        #     meals += meal

        for day in day_reference:
            try:
                meal_days_ids.append(day["id"])
                meals += day["meals"]
            except KeyError:
                day_id = created_days.pop(0).id
                meal_days_ids.append(day_id)
                for meal in day["meals"]:
                    meal["day"] = day_id
                    meals.append(meal)

        _, created_meals = model_services.perform_update(data=meals,
                                                         serializer=diet_serializers.MealSerializer,
                                                         context={"model": Meal,
                                                                  "fields": ("name",),
                                                                  "foreign_keys_fields": []},
                                                         many=True,
                                                         day__id__in=meal_days_ids)

        food_amount_meal_ids = []
        food_amount_list = []
        # for id, food_amount in [(meal["id"], meal["food_amount"]) for meal in meals]:
        #     food_amount_meal_ids.append(id)
        #     food_amount_list += food_amount

        for meal in meals:
            try:
                food_amount_meal_ids.append(meal["id"])
                food_amount_list += meal["food_amount"]
            except KeyError:
                meal_id = created_meals.pop(0).id
                food_amount_meal_ids.append(meal_id)
                for food_amount in meal["food_amount"]:
                    food_amount["meal"] = meal_id
                    food_amount_list.append(food_amount)

        model_services.perform_update(data=food_amount_list,
                                      serializer=diet_serializers.FoodAmountSerializer,
                                      context={"model": FoodAmount,
                                               "fields": ("grams",),
                                               "foreign_keys_fields": ("product",)},
                                      many=True,
                                      meal__id__in=food_amount_meal_ids)

        return Response(status=status.HTTP_200_OK)


class DayNutrientsViewSet(mixins.FilteredSearch, ModelViewSet):
    queryset = DayNutrients.objects.all()
    serializer_class = diet_serializers.DayNutrientsSerializer


class DietScheduleViewSet(mixins.FilteredSearch, ModelViewSet):
    queryset = DietSchedule.objects.all()
    serializer_class = diet_serializers.DietScheduleSerializer


class FoodAmountViewSet(mixins.FilteredSearch, ModelViewSet):
    queryset = FoodAmount.objects.all()
    serializer_class = diet_serializers.FoodAmountSerializer


class SupplementAmountViewSet(mixins.FilteredSearch, ModelViewSet):
    queryset = SupplementAmount.objects.all()
    serializer_class = diet_serializers.SupplementAmountSerializer


class MealViewSet(mixins.FilteredSearch, ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = diet_serializers.MealSerializer


class CustomMealViewSet(ModelViewSet):
    queryset = CustomMeal.objects.all()
    serializer_class = diet_serializers.CustomMealSerializer


class DietProgramDayViewSet(ModelViewSet):
    queryset = DietProgramDay.objects.all()
    serializer_class = diet_serializers.DietProgramDaySerializer

    @action(methods=["get"], detail=True, url_name="get_day_ref")
    def get_day_ref(self, request: Request, pk=None):
        queryset = self.get_queryset()\
            .filter(diet_program__id=pk)\
            # .prefetch_related("meals")
        print(queryset)
        serializer = self.get_serializer(queryset, many=True)
        print(serializer.data)
        headers = self.get_success_headers(serializer)
        return Response(status=status.HTTP_200_OK, data=serializer.data, headers=headers)
