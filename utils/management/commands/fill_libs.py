from django.core.management.base import BaseCommand, CommandError
from libs.models import Sport, MuscleGroup, Exercise, Product, Supplement
from faker import Faker


class Command(BaseCommand):
    help = "Fill library db with faker"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            'n', type=int, help='Lib stuff count to fill db with.')

    def handle(self, *args, **options):
        n = options['n']
        fake = Faker()

        for i in range(n):
            try:
                Exercise.objects.create(name=fake.text(
                    10)[:-1], description=fake.text(200))
                Product.objects.create(name=fake.text(
                    10)[:-1], calories=232.2, proteins=20., fats=2.4, carbohydrates=30.1)
                Sport.objects.create(name=fake.text(
                    15)[:-1], description=fake.text(160))
                MuscleGroup.objects.create(name=fake.text(
                    15)[:-1], functions=fake.text(100), description=fake.text(160))
                Supplement.objects.create(name=fake.text(
                    15)[:-1], daily_value=fake.random.random())

            except Exception as ex:
                print(ex)
