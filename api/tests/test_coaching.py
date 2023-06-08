from django.urls import reverse
from rest_framework.test import APITestCase
from cabinet.models import TgUser
from coaching.models import Client, ClientStatsActive, ClientStatsArchieved, ClientBaseExercises
from coaching.models import TrainingProgram, TrainingDay, ExerciseAmount
from ..serializers.coaching_serializers import TrainingDaySerializer
from mixer.backend.django import mixer
import json

# Create your tests here.


class TestCoachingViews(APITestCase):

    def setUp(self):
        self.user = mixer.blend(TgUser)
        self.another_user = mixer.blend(TgUser)
        self.coaching_client = mixer.blend(Client, coach=self.user)
        self.another_coaching_client = mixer.blend(
            Client, coach=self.another_user)
        self.training_program = mixer.blend(
            TrainingProgram, coach=self.user, client=self.coaching_client, time_start="2023-05-10", time_finish="2023-05-23")
        # self.training_exercises = mixer.blend(ExerciseAmount, day=)

        self.client.force_login(user=self.user)

    def test_client_list(self):
        response = self.client.get(reverse('client-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_client_invalid_create(self):
        response = self.client.post(reverse('client-list'), {
            'name': 'test_name',
            'telegram': 'test_telegram',
            'description': 'La la',
            'coach': '',
        })
        self.assertEqual(response.status_code, 400)

    def test_client_valid_create(self):
        # With sport tags
        response = self.client.post(reverse('client-list'), {
            'name': 'test_name',
            'telegram': 'test_telegram',
            'description': 'La la',
            'gender': 'M',
            'sport': self.coaching_client.sport.all(),
            'coach': self.user.id
        })
        # Without sport tags
        self.assertEqual(response.status_code, 201)
        response = self.client.post(reverse('client-list'), {
            'name': 'test_name',
            'telegram': 'test_telegram2',
            'description': 'La la',
            'gender': 'M',
            'coach': ''
        })
        self.assertEqual(response.status_code, 201)

    def test_client_get_all_info(self):
        response = self.client.get(
            reverse('client-info', kwargs={'pk': self.coaching_client.id}))
        self.assertIn("client", response.data)
        self.assertIn("stats", response.data)
        self.assertIn("base_exercises", response.data)
        self.assertEqual(self.user.id, response.data["client"]["coach"])
        self.assertEqual(self.coaching_client.id,
                         response.data["client"]["id"])
        self.assertEqual(response.status_code, 200)

    def test_client_stats_active_list(self):
        response = self.client.get(
            reverse('clientstats_active-list'))
        self.assertEqual(response.status_code, 200)

    def test_client_stats_archieved_list(self):
        response = self.client.get(
            reverse('clientstats_archieved-list'))
        self.assertEqual(response.status_code, 200)

    def test_client_base_exercises_list(self):
        response = self.client.get(
            reverse('client_base_exercises-list'))
        self.assertEqual(response.status_code, 200)

    def test_client_base_exercises_detail(self):
        response = self.client.get(
            reverse('client_base_exercises-detail', kwargs={'pk': self.coaching_client.id}))
        self.assertEqual(response.status_code, 200)

    def test_training_program_list(self):
        response = self.client.get(
            reverse('tprogram-list'))
        self.assertEqual(response.status_code, 200)

    def test_training_program_detail(self):
        response = self.client.get(
            reverse('tprogram-detail', kwargs={'pk': self.training_program.id}))
        self.assertEqual(response.status_code, 200)

    def test_training_program_get_program(self):
        response = self.client.get(
            reverse('tprogram-get_program', kwargs={'pk': self.training_program.id}))

        self.assertIn("days", response.data)
        self.assertEqual(response.data["days"][0]["program"],
                         self.training_program.id)
        self.assertIn("exercises", response.data["days"][0])
        self.assertEqual(response.data["id"], self.training_program.id)
        self.assertEqual(response.status_code, 200)

    def test_training_program_invalid_create(self):
        response = self.client.post(reverse('tprogram-list'), {
            'name': 'test_name',
            'description': 'test_description',
            'time_start': '10.05.2023',
            'time_finish': '23.05.2023',
            'client': "",
        })
        self.assertEqual(response.status_code, 400)

    def test_training_program_valid_create(self):
        response = self.client.post(reverse('tprogram-list'), {
            'name': 'test_name',
            'description': 'test_description',
            'time_start': '08.05.2023',
            'time_finish': '28.05.2023',
            'client': self.coaching_client.id,
        })
        self.assertEqual(response.status_code, 201)

    def test_training_program_update(self):
        days = TrainingDay.objects.filter(
            program=self.training_program)

        serializer = TrainingDaySerializer(instance=days, many=True)
        print(serializer.data)
        data = serializer.data

        for day in data:
            day["exercises"] = []
        weeks = []
        while data:
            weeks.append(data[:7])
            data = data[7:]

        response = self.client.put(
            reverse("tprogram-detail",
                    kwargs={'pk': self.training_program.id}), data=json.dumps({
                        'name': 'test_name',
                        'description': 'test_description',
                        'time_start': '10.05.2023',
                        'time_finish': '23.05.2023',
                        'client': self.coaching_client.id,
                        'weeks': weeks
                    }), content_type="application/json"
        )

        self.assertEqual(response.status_code, 202)
