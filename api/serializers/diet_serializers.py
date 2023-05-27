from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from api.serializers.libs_serializers import SupplementSerializer, FoodSerializer
# Diet Serializers
from diet.models import DietProgram, DayNutrients, DietSchedule, FoodAmount
from diet.models import SupplementAmount, Meal, CustomMeal, DietProgramDay

from . import BulkUpdateOrCreateListSerializer
from . import libs_serializers


class DietProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietProgram
        exclude = ("recommended_products", "forbidden_products")

    def update(self, instance, validated_data):
        print(validated_data)
        return super().update(instance, validated_data)


class ExtendedDietProgramSerializer(serializers.ModelSerializer):
    recommended_products = libs_serializers.FoodSerializer(many=True)
    forbidden_products = libs_serializers.FoodSerializer(many=True)
    schedule = serializers.SerializerMethodField()
    nutrients = serializers.SerializerMethodField()
    day_reference = serializers.SerializerMethodField()

    class Meta:
        model = DietProgram
        fields = "__all__"

    def get_nutrients(self, obj):
        queryset = obj.nutrients.all()
        serializer = DayNutrientsSerializer(
            queryset, many=True)
        return serializer.data

    def get_schedule(self, obj):
        queryset = obj.schedule.all()
        serializer = DietScheduleSerializer(
            queryset, many=True)
        return serializer.data

    def get_day_reference(self, obj):
        queryset = obj.day_reference.all()
        serializer = DietProgramDaySerializer(
            queryset, many=True)
        return serializer.data

    def update(self, instance, validated_data):
        # Переопределяем метод для вложенной сериализации М2М полей.
        recommended_products = validated_data.pop("recommended_products")
        forbidden_products = validated_data.pop("forbidden_products")
        validated_data["recommended_products"] = list(
            map(lambda x: x["id"], recommended_products))
        validated_data["forbidden_products"] = list(
            map(lambda x: x["id"], forbidden_products))

        m2m_fields = []
        for attr, value in validated_data.items():

            # Явно указываем поля
            if attr == "recommended_products" or attr == "forbidden_products":
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance


class DayNutrientsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = DayNutrients
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer


class DietScheduleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = DietSchedule
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer

    # def update(self, instance, validated_data):
    #     print(instance)
    #     print(validated_data)
    #     return super().update(instance, validated_data)


class FoodAmountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    product = FoodSerializer()

    class Meta:
        model = FoodAmount
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer

    def update(self, instance, validated_data):
        print("AOAOAOOAOAAOOOOOAOAOOA")
        validated_data["product"] = validated_data["product"].get("id")
        return {}
        # return super().update(instance, validated_data)


class SupplementAmountSerializer(serializers.ModelSerializer):

    name = SupplementSerializer()

    class Meta:
        model = SupplementAmount
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer


class MealSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    food_amount = serializers.SerializerMethodField()

    class Meta:
        model = Meal
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer

    def get_food_amount(self, obj):
        food_amount = obj.foodamount.all().select_related("product")
        serializer = FoodAmountSerializer(food_amount, many=True)
        return serializer.data


class CustomMealSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomMeal
        fields = "__all__"


class DietProgramDaySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    meals = serializers.SerializerMethodField()

    class Meta:
        model = DietProgramDay
        fields = "__all__"
        list_serializer_class = BulkUpdateOrCreateListSerializer

    def get_meals(self, obj):
        meals = obj.meals.all().prefetch_related("foodamount")
        serializer = MealSerializer(meals, many=True)
        return serializer.data
