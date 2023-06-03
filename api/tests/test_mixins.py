from django.urls import reverse
from rest_framework.test import APITestCase
from mixer.backend.django import mixer
from cabinet.models import TgUser
from libs.models import Exercise, Sport, MuscleGroup


class TestMixins(APITestCase):

    def setUp(self):
        self.user = mixer.blend(TgUser)
        self.sports = [mixer.blend(Sport) for i in range(3)]
        self.muscle_groups = [mixer.blend(MuscleGroup) for i in range(6)]
        self.exercises = []
        for sport in self.sports:
            self.exercises += [mixer.blend(Exercise, sport=sport)
                               for i in range(4)]
        self.add_m2m()
        self.client.force_login(user=self.user)

    def add_m2m(self):
        """
        Добавляем м2м чтобы проверить их выборку методом chain_filter из mixin'ов.
        У упражнения 2 должны быть мг из первого и второго цикла.
        """
        for exercise in self.exercises[:3]:
            [exercise.muscle.add(muscle_group.id)
             for muscle_group in self.muscle_groups[:2]]

        for exercise in self.exercises[2:]:
            [exercise.muscle.add(muscle_group.id)
             for muscle_group in self.muscle_groups[3:5]]

    def test_list_filter(self):
        """
        Тест mixin'а для филтрации.
        """
        response = self.client.get(
            reverse('exercise-filter'))

        self.assertEqual(len(response.data), 12)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse('exercise-filter'), QUERY_STRING=f"sport={self.sports[0].id}")

        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, 200)

    def test_list_chained_filter(self):
        """
        Тест для проверки mixin'а для филтрации m2m полей.
        """
        response = self.client.get(reverse('exercise-filter'))
        print("data", response.data)
        self.assertEqual(len(response.data), 12)

        response = self.client.get(
            reverse('exercise-chain_filter'),
            QUERY_STRING=f"muscle={self.muscle_groups[0].id},{self.muscle_groups[1].id}")
        self.assertEqual(len(response.data), 3)

        response = self.client.get(
            reverse('exercise-chain_filter'),
            QUERY_STRING=f"muscle={self.muscle_groups[0].id},{self.muscle_groups[3].id}")
        self.assertEqual(len(response.data), 1)

        response = self.client.get(
            reverse('exercise-chain_filter'),
            QUERY_STRING=f"muscle={self.muscle_groups[3].id},{self.muscle_groups[4].id}")
        self.assertEqual(len(response.data), 10)

        self.assertEqual(response.status_code, 200)
