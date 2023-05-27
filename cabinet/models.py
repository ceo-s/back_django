from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save


class TgUser(AbstractUser):
    telegram = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.username


def path_prof_pic(instance, filename):
    return f"profile_pics/{instance.user.username}/{filename}"


class ProfileCard(models.Model):
    user = models.OneToOneField(
        to="TgUser", to_field="username", on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(
        max_length=150, unique=False, default="Имя Фамилия")
    profile_pic = models.ImageField(
        upload_to=path_prof_pic, default="profile_pics/8r9pym5wqg4t.jpg")

    sport = models.ManyToManyField(to="libs.Sport", blank=True)
    bio = models.TextField(default="Введите информацию о себе...")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


def path_post_pic(instance, filename):
    return f"posts/{instance.user.username}/{filename[:99]}"


class Post(models.Model):
    user = models.ForeignKey(to="TgUser",
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=511)
    content = models.TextField()
    media = models.ImageField(upload_to=path_post_pic, null=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


@receiver(post_save, sender=TgUser)
def create_profile(sender, instance, **kwargs):
    """Создаёт модель ProfileCard и Coaching при регистрации пользователя"""
    if kwargs['created']:
        ProfileCard.objects.create(user=instance)
