from django.urls import reverse
from rest_framework.test import APITestCase
from mixer.backend.django import mixer
from cabinet.models import TgUser
from libs.models import Exercise, Sport, MuscleGroup, Product, Supplement


class TestLibsViews(APITestCase):

    def setUp(self):
        self.user = mixer.blend(TgUser)
        self.exercise = mixer.blend(Exercise)
        self.sport = mixer.blend(Sport)
        self.muscle_group = mixer.blend(MuscleGroup)
        self.food = mixer.blend(Product)
        self.supplement = mixer.blend(Supplement)
        self.client.force_login(user=self.user)

    def test_exercise_list(self):
        response = self.client.get(reverse('exercise-list'))
        self.assertEqual(response.status_code, 200)

    def test_exercise_detail(self):
        response = self.client.get(
            reverse('exercise-detail', kwargs={'pk': self.exercise.id}))
        self.assertEqual(response.status_code, 200)

    def test_sport_list(self):
        response = self.client.get(reverse('sport-list'))
        self.assertEqual(response.status_code, 200)

    def test_sport_detail(self):
        response = self.client.get(
            reverse('sport-detail', kwargs={'pk': self.sport.id}))
        self.assertEqual(response.status_code, 200)

    def test_muscle_group_list(self):
        response = self.client.get(reverse('muscle-list'))
        self.assertEqual(response.status_code, 200)

    def test_muscle_group_detail(self):
        response = self.client.get(
            reverse('muscle-detail', kwargs={'pk': self.muscle_group.id}))
        self.assertEqual(response.status_code, 200)

    def test_food_list(self):
        response = self.client.get(reverse('food-list'))
        self.assertEqual(response.status_code, 200)

    def test_food_detail(self):
        response = self.client.get(
            reverse('food-detail', kwargs={'pk': self.food.id}))
        self.assertEqual(response.status_code, 200)

    def test_supplement_list(self):
        response = self.client.get(reverse('supplements-list'))
        self.assertEqual(response.status_code, 200)
