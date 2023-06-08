from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from utils.services import date_time_fuctions


# Create your models here.


class Client(models.Model):
    """
    Coaching client.
    """
    # Gender options
    MALE = "M"
    FEMALE = "W"
    GENDER_CHOICES = [
        (MALE, "Man"),
        (FEMALE, "Woman")
    ]
    name = models.CharField(max_length=127)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    telegram = models.CharField(
        max_length=100, null=True, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)
    sport = models.ManyToManyField(to="libs.Sport", blank=True)
    coach = models.ForeignKey(
        to="cabinet.TgUser", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class ClientStats(models.Model):
    """
    Abstract measurements model.
    """
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    bodyfat_percent = models.FloatField(null=True, blank=True)
    neck = models.FloatField(null=True, blank=True)
    shoulders = models.FloatField(null=True, blank=True)
    chest = models.FloatField(null=True, blank=True)
    bicep = models.FloatField(null=True, blank=True)
    forearm = models.FloatField(null=True, blank=True)
    waist = models.FloatField(null=True, blank=True)
    glutes = models.FloatField(null=True, blank=True)
    legs = models.FloatField(null=True, blank=True)
    calves = models.FloatField(null=True, blank=True)

    class Meta:
        abstract = True


class ClientStatsActive(ClientStats):
    """
    Client statistic and measurements current.
    """
    client = models.OneToOneField(
        to="Client", on_delete=models.CASCADE, primary_key=True)
    date_update = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"Stats of {self.client.name}"

    class Meta:
        verbose_name = "Статистика клиента"
        verbose_name_plural = "Статистика клиентов"


class ClientStatsArchieved(ClientStats):
    """
    Client statistic and measurements archieve.
    """
    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    date_created = models.DateField()
    date_archieved = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Archieved stats of {self.client}"

    class Meta:
        verbose_name = "Архивная статистика клиента"
        verbose_name_plural = "Архивная статистика клиентов"


class ClientBaseExercises(models.Model):
    """
    Client exercises for statistic display.
    """
    client = models.OneToOneField(
        "Client", on_delete=models.CASCADE)
    exercises = models.ManyToManyField(to='libs.Exercise')

    def __str__(self) -> str:
        return f"Base exercises of {self.client}"

    class Meta:
        verbose_name = "Упражнения для отслеживания статистики"
        verbose_name_plural = "Упражнения для отслеживания статистики"


class TrainingProgram(models.Model):
    """
    Client training program.
    """
    coach = models.ForeignKey(
        to="cabinet.TgUser", on_delete=models.CASCADE)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=127, default="Новая программа")
    description = models.TextField()
    time_start = models.DateField()
    time_finish = models.DateField()

    # FIXME перестала работать :)
    def save(self, *args, **kwargs) -> None:
        self.time_start = date_time_fuctions.weekstart_date(self.time_start)
        self.time_finish = date_time_fuctions.weekend_date(self.time_finish)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Программа тренировок"
        verbose_name_plural = "Программы тренировок"


class TrainingDay(models.Model):
    """
    Training day for training program.
    """
    program = models.ForeignKey(
        to="TrainingProgram", on_delete=models.CASCADE, related_name="days")
    date = models.DateField()

    def __str__(self) -> str:
        return f"{self.date}"

    class Meta:
        verbose_name = "Тренироваочный день"
        verbose_name_plural = "Тренировочные дни"


class ExerciseAmount(models.Model):
    """
    Exercise configuration for training day.
    """
    exercise = models.ForeignKey(
        to="libs.Exercise", on_delete=models.CASCADE, null=True)
    name = models.CharField(blank=True)
    count = models.IntegerField()
    reps = models.IntegerField(null=True)
    sets = models.IntegerField(null=True)
    weight = models.FloatField(null=True)
    comment = models.TextField(blank=True)
    training_day = models.ForeignKey(
        to="TrainingDay", on_delete=models.CASCADE, related_name="examount")

    class Meta:
        verbose_name = "Запись об упражнениях"
        verbose_name_plural = "Записи об упражнениях"


@receiver(post_save, sender=Client)
def on_client_creation(sender, instance, **kwargs):
    """On client creation:
       - creates ClientStatsActive instanse
       - creates ClientBaseExercises instance."""
    if kwargs['created']:
        ClientStatsActive.objects.create(client=instance)
        ClientBaseExercises.objects.create(
            client=instance)
        # FIXME
        # exercises = apps.get_model('libs', 'Exercise').get_base_exercises()
        # client_base_exercises.exercises.add(*exercises)


@receiver(post_save, sender=TrainingProgram)
def fill_program(sender, instance, **kwargs):
    """
    Create training days related to Created TrainingProgram.
    """
    if kwargs['created']:
        days = date_time_fuctions.get_interval_dates(
            str(instance.time_start), str(instance.time_finish))
        training_days = [TrainingDay(program=instance, date=day)
                         for day in days]
        TrainingDay.objects.bulk_create(training_days)
