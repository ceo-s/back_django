import io
from PIL import Image
from mixer.backend.django import mixer
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import TgUser, ProfileCard, Post, path_post_pic, path_prof_pic

# Create your tests here.


class TestCabinet(TestCase):
    """
    Unit tests for cabinet app.
    """

    def setUp(self):
        image = io.BytesIO()
        Image.new("RGB", (1080, 1080)).save(image, "JPEG")
        image.seek(0)

        self.filename = "simple_image"
        self.file = SimpleUploadedFile(self.filename, image.getvalue())

        self.tg_user = mixer.blend(
            TgUser, telegram="qwerty")
        self.posts_count = 3
        self.posts = [mixer.blend(Post, user=self.tg_user, media=self.file)
                      for i in range(self.posts_count)]

    def test_telegram(self):
        """
        Tests if telegram is created and equal to username.
        """
        tg_user = self.tg_user  # type: ignore
        self.assertEqual(tg_user.telegram, "qwerty")
        self.assertEqual(str(tg_user), tg_user.username)

    def test_profile_creation_single(self):
        """
        Tests if profile been crated by signal recieving on user creation.
        """
        profiles = ProfileCard.objects.all()
        self.assertEqual(1, len(profiles))

    def test_profile_creation(self):
        """
        Tests if profile and user are connected and related fields are equal.
        """
        profile = ProfileCard.objects.get(user=self.tg_user)
        self.assertEqual(self.tg_user, profile.user)
        self.assertEqual(str(profile), profile.name)

    def test_posts_creation(self):
        """
        Tests if posts were created correctly.
        """
        posts = Post.objects.filter(user=self.tg_user)
        self.assertEqual(self.posts_count, len(posts))
        self.assertEqual(str(posts[0]), posts[0].title)

    def test_path_post_pic(self):
        """
        Tests if path to post picture was generated correctly.
        """
        self.assertEqual(self.posts[0].media, path_post_pic(
            self.posts[0], self.filename))

    def test_path_prof_pic(self):
        """
        Tests if path to profile picture was generated correctly.
        """
        profile = ProfileCard.objects.get(user=self.tg_user)
        profile.profile_pic = self.file  # type: ignore
        profile.save()
        self.assertEqual(profile.profile_pic, path_prof_pic(
            profile, self.filename))
