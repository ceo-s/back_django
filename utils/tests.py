from django.test import TestCase
from .services.date_time_fuctions import get_weeks_count
from datetime import timedelta, datetime
# Create your tests here.


class TestUtils(TestCase):

    def test_get_weeks_count(self):
        today = datetime.today()
        end_day = today + timedelta(7*2)
        weeks = list(get_weeks_count(today.strftime(
            "%Y-%m-%d"), end_day.strftime("%Y-%m-%d")))
        self.assertEqual(len(weeks), 2)

        today = datetime.today()
        end_day = today + timedelta(13)
        weeks = list(get_weeks_count(today.strftime(
            "%Y-%m-%d"), end_day.strftime("%Y-%m-%d")))
        self.assertEqual(len(weeks), 1)

        today = datetime.today()
        end_day = today + timedelta(15)
        weeks = list(get_weeks_count(today.strftime(
            "%Y-%m-%d"), end_day.strftime("%Y-%m-%d")))
        self.assertEqual(len(weeks), 2)
