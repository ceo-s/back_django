from django.core.management.base import BaseCommand, CommandError
from cabinet.models import TgUser
from coaching.models import Client, ClientStatsActive
from cabinet.models import ProfileCard
from faker import Faker
import random


class Command(BaseCommand):
    help = "Fill db with faker users"

    def add_arguments(self, parser) -> None:
        parser.add_argument('n', type=int, help='Users count to fill db with.')
        parser.add_argument(
            'm', type=int, help='Clients for each coach count.')

    def handle(self, *args, **options):
        n = options['n']
        m = options['m']

        fake = Faker()
        for i in range(n):
            try:
                username = fake.user_name()
                new_user = TgUser.objects.create(
                    username=username, password=0, telegram=username)
            except Exception as ex:
                print(ex)

            ProfileCard.objects.filter().update()
            # coach = Coach.objects.get(user=new_user)
            user_profile = ProfileCard.objects.get(user=new_user)
            user_profile.name = fake.name()
            user_profile.bio = fake.text(300)
            user_profile.save()

            for i in range(m):
                try:
                    new_client = Client.objects.create(name=fake.name(
                    ), telegram=fake.user_name(), description=fake.text(100), coach=new_user)
                    # ClientStats.objects.create(client=new_client, height=random.gauss(180, 7), weight=random.gauss(90, 10))
                except Exception as ex:
                    print(ex)

        users = TgUser.objects.all()
        for user in users:
            user_profile = ProfileCard.objects.get(user=user)

        for i in range(m):
            me = TgUser.objects.get(id=1)
            new_client = Client.objects.create(
                name=f"Валера{i}", telegram=f"valetiy{i}", description=fake.text(100), coach=me)
