from django.urls import reverse
from rest_framework.test import APITestCase
from cabinet.models import TgUser
from coaching.models import Client
from diet.models import DietProgram, DietProgramDay, DietSchedule, DayNutrients
from diet.models import Meal, CustomMeal, FoodAmount, CustomMealFoodAmount
from ..serializers.diet_serializers import DietScheduleSerializer, DayNutrientsSerializer, DietProgramDaySerializer
from mixer.backend.django import mixer
import json


class TestDietViews(APITestCase):

    def setUp(self):
        self.user = mixer.blend(TgUser)
        self.client.force_login(user=self.user)
        self.coaching_client = mixer.blend(Client, coach=self.user)
        self.diet_program = mixer.blend(
            DietProgram, coach=self.user, client=self.coaching_client)
        self.diet_program_day = mixer.blend(
            DietProgramDay, diet_program=self.diet_program)
        self.meal = mixer.blend(Meal, day=self.diet_program_day)
        self.day_nutrients = mixer.blend(
            DayNutrients, diet_program=self.diet_program)
        self.diet_schedule = mixer.blend(
            DietSchedule, program=self.diet_program, day_type=self.day_nutrients)
        self.custom_meal = mixer.blend(
            CustomMeal, coach=self.user)

    def test_diet_program_list(self):
        response = self.client.get(reverse("dprogram-list"))
        self.assertEqual(response.status_code, 200)

    def test_diet_program_detail(self):
        response = self.client.get(
            reverse("dprogram-detail", kwargs={"pk": self.diet_program.id}))
        self.assertEqual(response.status_code, 200)

    def test_diet_program_invalid_create(self):
        self.client.logout()
        data = {
            "name": "test",
            "client": self.coaching_client.id,
        }
        response = self.client.post(reverse("dprogram-list"), data=data)
        self.assertEqual(response.status_code, 400)

    def test_diet_program_valid_create(self):
        data = {
            "name": "test",
            "client": self.coaching_client.id,
        }
        response = self.client.post(reverse("dprogram-list"), data=data)
        self.assertEqual(response.data['coach'], self.user.id)
        self.assertEqual(response.data['client'], self.coaching_client.id)
        self.assertEqual(response.status_code, 201)

    def test_diet_program_update(self):

        schedule = [DietScheduleSerializer(instance=self.diet_schedule).data]
        nutrients = [DayNutrientsSerializer(instance=self.day_nutrients).data]
        days = [DietProgramDaySerializer(instance=self.diet_program_day).data]

        response = self.client.put(
            reverse("dprogram-detail", kwargs={"pk": self.diet_program.id}),
            data=json.dumps({
                'recommended_products': [],
                'forbidden_products': [],
                'schedule': schedule,
                'nutrients': nutrients,
                'day_reference': days,
                'name': 'O yeah',
                'description': 'Yeah',
                'date_start': '10.05.2023',
                'date_finish': '26.05.2023',
                'coach': self.user.id,
                'client': self.coaching_client.id,
            }), content_type="application/json"
        )
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_diet_program_get_program(self):
        response = self.client.get(
            reverse("dprogram-get_program", kwargs={"pk": self.diet_program.id}))

        self.assertIn("schedule", response.data)
        self.assertIn("nutrients", response.data)
        self.assertIn("day_reference", response.data)
        self.assertEqual(response.data["coach"], self.user.id)
        self.assertEqual(response.data["client"], self.coaching_client.id)
        self.assertEqual(response.status_code, 200)

    def test_diet_program_day_get_day_ref(self):
        response = self.client.get(
            reverse("diet_day-get_day_ref", kwargs={"pk": self.diet_program.id}))

        self.assertEqual(response.status_code, 200)
