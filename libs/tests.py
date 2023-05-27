from django.test import TestCase
from . import models
from mixer.backend.django import mixer

# Create your tests here.


class TestLibs(TestCase):
    def setUp(self):
        self.sport = mixer.blend(models.Sport)
        self.muscle_group = mixer.blend(models.MuscleGroup)
        self.exercise = mixer.blend(models.Exercise)
        self.product = mixer.blend(models.Product)
        self.supplement = mixer.blend(models.Supplement)
        self.add_m2m()

    def add_m2m(self):
        self.exercise.muscle.add(self.muscle_group)
        self.exercise.sport_tag.add(self.sport)

    def test_sport(self):
        exercises = self.sport.exercise_set.all()
        self.assertEqual(exercises[0], self.exercise)
        self.assertEqual(self.sport.__str__(), self.sport.name)

    def test_muscle_group(self):
        exercises = self.muscle_group.exercise_set.all()
        self.assertEqual(exercises[0], self.exercise)
        self.assertEqual(self.muscle_group.__str__(), self.muscle_group.name)

    def test_exercise(self):
        sports = self.exercise.sport_tag.all()
        muscle_groups = self.exercise.muscle.all()
        self.assertEqual(muscle_groups[0], self.muscle_group)
        self.assertEqual(sports[0], self.sport)
        self.assertEqual(self.exercise.__str__(), self.exercise.name)

    def test_product(self):
        self.assertEqual(self.product.__str__(), self.product.name)

    def test_supplement(self):
        self.assertEqual(self.supplement.__str__(), self.supplement.name)
