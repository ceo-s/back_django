from mixer.backend.django import mixer
from django.test import TestCase
from cabinet.models import TgUser
from coaching.models import Client
from libs.models import Product
from . import models

# Create your tests here.


class TestDiet(TestCase):
    """
    Unit tests for diet program in diet app.
    """

    def setUp(self):
        self.coach = mixer.blend(TgUser)
        self.coaching_client = mixer.blend(Client, coach=self.coach)
        self.diet_program = mixer.blend(
            models.DietProgram, coach=self.coach, client=self.coaching_client)
        self.add_m2m(4, 7)

    def add_m2m(self, recommended_products_count, forbidden_products_count):
        """
        Adds many to many fields to related model.
        """
        self.products = [mixer.blend(Product) for i in range(
            recommended_products_count + forbidden_products_count + 10)]
        program = models.DietProgram.objects.get(coach=self.coach)

        for product in self.products[:recommended_products_count]:
            program.recommended_products.add(product)

        for product in self.products[recommended_products_count+5:recommended_products_count+5+forbidden_products_count]:
            program.forbidden_products.add(product)

    def test_diet_program(self):
        """
        Tests if programs are creating porperly.
        """
        programs = models.DietProgram.objects.all()
        self.assertEqual(1, len(programs))
        self.assertEqual(programs[0].coach, self.coach)
        self.assertEqual(programs[0].client, self.coaching_client)
        self.assertEqual(str(self.diet_program), self.diet_program.name)

    def test_m2m_fields(self):
        """
        Tests many to many fields count, based on addad m2m before.
        """
        self.assertEqual(len(self.diet_program.recommended_products.all()), 4)
        self.assertEqual(len(self.diet_program.forbidden_products.all()), 7)


class TestDietNutrients(TestCase):
    """
    Unit tests for nutrients in diet app.
    """

    def setUp(self):
        self.coach = mixer.blend(TgUser)
        self.coaching_client = mixer.blend(Client, coach=self.coach)
        self.diet_program = mixer.blend(
            models.DietProgram, coach=self.coach, client=self.coaching_client)
        self.nutrients = [mixer.blend(
            models.DayNutrients, diet_program=self.diet_program) for i in range(3)]
        self.schedule_days = [models.DietSchedule(count=i+1,
                                                  day_type=mixer.faker.random.choice(
                                                      self.nutrients),
                                                  program=self.diet_program).save() for i in range(7)]

    def test_nutrients(self):
        """
        Tests if nutrients are creating properly.
        """
        nutrients = models.DayNutrients.objects.all()
        self.assertEqual(len(nutrients), len(self.nutrients))
        self.assertEqual(nutrients[0].diet_program, self.diet_program)
        self.assertEqual(str(nutrients[0]), nutrients[0].name)

    def test_diet_schedule(self):
        """
        Tests if diet schedule is creating properly.
        """
        schedule_days = models.DietSchedule.objects.all()
        self.assertEqual(len(schedule_days), len(self.schedule_days))
        self.assertEqual(schedule_days[0].program, self.diet_program)
        self.assertEqual(schedule_days[0].count, 1)
        self.assertIn(schedule_days[0].day_type, self.nutrients)
        self.assertEqual(str(schedule_days[0]),
                         str(schedule_days[0].count))


class TestDietDay(TestCase):
    """
    Unit tests for diet days in diet app.
    """

    def setUp(self):
        self.coach = mixer.blend(TgUser)
        self.coaching_client = mixer.blend(Client, coach=self.coach)
        self.diet_program = mixer.blend(
            models.DietProgram, coach=self.coach, client=self.coaching_client)
        self.create_days(3)

    def create_days(self, n):
        """
        Creates reference days.
        """
        diet_days = [mixer.blend(models.DietProgramDay,
                                 diet_program=self.diet_program) for i in range(n)]
        meals = []
        for day in diet_days:
            meals.extend([mixer.blend(models.Meal, day=day) for i in range(n)])

        food_amounts = []
        for meal in meals:
            food_amounts.extend(
                [mixer.blend(models.FoodAmount, meal=meal) for i in range(n)])

        self.diet_days = diet_days
        self.meals = meals
        self.food_amounts = food_amounts

    def test_diet_day(self):
        """
        Tests if diet days are creating properly.
        """
        self.assertEqual(str(self.diet_days[0]), self.diet_days[0].name)

    def test_meals(self):
        """
        Tests if meals are creating properly.
        """
        meals = models.Meal.objects.all()
        self.assertEqual(len(meals), len(self.meals))
        self.assertEqual(str(meals[0]), meals[0].name)

    def test_food_amouunts(self):
        """
        Tests if food amounts are creating properly.
        """
        food_amounts = models.FoodAmount.objects.all()
        self.assertEqual(len(food_amounts), len(self.food_amounts))
        self.assertEqual(
            str(food_amounts[0]), f"{food_amounts[0].product} - {food_amounts[0].grams}")

    def test_reverse_relations(self):
        """
        Tests if all reverse relations are working.
        """
        days = self.diet_program.day_reference.all()
        meals = self.diet_days[0].meals.all()
        foods = self.meals[0].foodamount.all()

        self.assertEqual(len(days), len(
            models.DietProgramDay.objects.filter(diet_program=self.diet_program)))

        self.assertEqual(len(meals), len(
            models.Meal.objects.filter(day=self.diet_days[0])))

        self.assertEqual(len(foods), len(
            models.FoodAmount.objects.filter(meal=self.meals[0])))

    def test_relations(self):
        """
        Tests if all relations are working.
        """
        days = models.DietProgramDay.objects.filter(
            diet_program=self.diet_program)
        meals = models.Meal.objects.filter(day=days[0])
        foods = models.FoodAmount.objects.filter(meal=meals[0])

        self.assertEqual(len(days), len(
            models.DietProgramDay.objects.filter(diet_program=self.diet_program)))

        self.assertEqual(len(meals), len(
            models.Meal.objects.filter(day=self.diet_days[0])))

        self.assertEqual(len(foods), len(
            models.FoodAmount.objects.filter(meal=self.meals[0])))
