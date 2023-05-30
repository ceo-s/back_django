from mixer.backend.django import mixer
from django.test import TestCase
from cabinet.models import TgUser
from utils.services import date_time_fuctions
from . import models

# Create your tests here.


class TestCoachingClients(TestCase):
    """
    Unit tests for clients in coaching app.
    """

    def setUp(self):
        self.coach = mixer.blend(TgUser)
        self.coaching_client = mixer.blend(
            models.Client, coach=self.coach)

    def test_client_creation(self):
        """
        Tests if client is created correctly with relation to coach.
        """
        clients = models.Client.objects.all()
        self.assertEqual(1, len(clients))
        self.assertEqual(clients[0].coach, self.coach)
        self.assertEqual(str(clients[0]), clients[0].name)

    def test_client_stats_active(self):
        """
        Tests if active stats instance was created on recieved signal from client creation.
        """
        stats = models.ClientStatsActive.objects.all()
        self.assertEqual(1, len(stats))
        self.assertEqual(stats[0].client, self.coaching_client)
        self.assertEqual(str(stats[0]),
                         f"Stats of {self.coaching_client}")

    def test_client_stats_archieved(self):
        """
        Tests if archieved stats are creating properly.
        """
        stats = mixer.blend(models.ClientStatsArchieved,
                            client=self.coaching_client)
        self.assertEqual(
            str(stats), f"Archieved stats of {self.coaching_client.name}")

    def test_client_base_exercises(self):
        """
        Tests if client base exercises are creating properly.
        """
        base_exercises = models.ClientBaseExercises.objects.all()
        self.assertEqual(1, len(base_exercises))
        self.assertEqual(base_exercises[0].client, self.coaching_client)
        self.assertEqual(str(base_exercises[0]),
                         f"Base exercises of {self.coaching_client}")


class TestTrainingProgram(TestCase):
    """
    Unit tests for training programs in coaching app.
    """

    def setUp(self):
        self.coach = mixer.blend(TgUser)
        self.coaching_client = mixer.blend(models.Client, coach=self.coach)
        self.training_program = mixer.blend(models.TrainingProgram,
                                            time_start="2023-05-23",
                                            time_finish="2023-10-23",
                                            client=self.coaching_client)

    def test_training_program_str(self):
        """
        Dummy str test.
        """
        self.assertEqual(str(self.training_program),
                         self.training_program.name)

    def test_training_program_day_str(self):
        """
        Dummy str test.
        """
        first_day = models.TrainingDay.objects.all()[0]
        self.assertEqual(str(first_day), str(first_day.date))

    def test_training_program_days(self):
        """
        Tests if program days are created with correct date range.
        """
        training_program = models.TrainingProgram.objects.get(
            id=self.training_program.id)
        start = training_program.time_start
        finish = training_program.time_finish
        first_day = models.TrainingDay.objects.all()[0]
        last_day = models.TrainingDay.objects.order_by("-id")[0]
        self.assertEqual(start, first_day.date)
        self.assertEqual(finish, last_day.date)

    def test_training_program_days_count(self):
        """
        Tests if program days are created with right quantity.
        """
        start = self.training_program.time_start
        finish = self.training_program.time_finish
        interval = date_time_fuctions.get_interval_dates(start, finish)
        self.assertEqual(models.TrainingDay.objects.count(), len(interval))
