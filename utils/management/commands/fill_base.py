from django.core.management.base import BaseCommand, CommandError
from cabinet.models import TgUser
from libs.models import Sport
from faker import Faker
import random

sports = {
    "Powerlifting": "Powerlifting is a strength sport that consists of three attempts at maximal weight on three lifts: squat, bench press, and deadlift.",
    "Streetlifting": "Streetlifting (Стритлифтинг) — includes two movements: pull-up (chin-up) on the crossbar and dips with additional weights.",
    "Bodybuilding": "Bodybuilding is the use of progressive resistance exercise to control and develop one's muscles (muscle building) by muscle hypertrophy for aesthetic purpouses.",
    "Fitness": "Fitness is is having a healthy mind, body, and spirit to allow you to maximize your potential and help others maximize their potential.",
    "Calistenics": "Calisthenics (American English) or callisthenics (British English) (/ˌkælɪsˈθɛnɪks/) is a form of strength training consisting of a variety of movements that exercise large muscle groups (gross motor movements), such as standing, grasping, pushing, etc.",
}

experience = {
    "<1": "Noob",
    "1-2": "Dumb fuck",
    "2-5": "Cool guy",
    "5-10": "Grandmaster",
    "10<": "Gym boss",
}


class Command(BaseCommand):
    help = "Fill db with base information. Should be used on very begining."

    def handle(self, *args, **options):
        for sport, description in sports.items():
            try:
                Sport.objects.create(name=sport, description=description)
            except Exception as ex:
                print(ex)

        # for time, status in experience.items():
        #     try:
        #         Experience.objects.create(time=time, status=status)
        #     except Exception as ex:
        #         print(ex)
