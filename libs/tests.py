from mixer.backend.django import mixer
from django.test import TestCase
from . import models

# Create your tests here.


class TestLibs(TestCase):
    """
    Unit tests for the libs app.
    """

    def setUp(self):
        self.sport = mixer.blend(models.Sport)
        self.muscle_group = mixer.blend(models.MuscleGroup)
        self.exercise = mixer.blend(models.Exercise)
        self.product = mixer.blend(models.Product)
        self.supplement = mixer.blend(models.Supplement)
        self.add_m2m()

    def add_m2m(self):
        """
        Adds many to many fields to related model.
        """
        self.exercise.muscle.add(self.muscle_group)
        self.exercise.sport.add(self.sport)

    def test_sport(self):
        """
        Tests if sport instance is created properly.
        """
        exercises = self.sport.exercise_set.all()
        self.assertEqual(exercises[0], self.exercise)
        self.assertEqual(str(self.sport), self.sport.name)

    def test_muscle_group(self):
        """
        Tests if muscle group instance is created properly.
        """
        exercises = self.muscle_group.exercise_set.all()
        self.assertEqual(exercises[0], self.exercise)
        self.assertEqual(str(self.muscle_group), self.muscle_group.name)

    def test_exercise(self):
        """
        Tests if exercise instance is created properly.
        """
        sports = self.exercise.sport.all()
        muscle_groups = self.exercise.muscle.all()
        self.assertEqual(muscle_groups[0], self.muscle_group)
        self.assertEqual(sports[0], self.sport)
        self.assertEqual(str(self.exercise), self.exercise.name)

    def test_product(self):
        """     
        Dummy str test.
        """
        self.assertEqual(str(self.product), self.product.name)

    def test_supplement(self):
        """     
        Dummy str test.
        """
        self.assertEqual(str(self.supplement), self.supplement.name)
