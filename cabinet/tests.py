from django.test import TestCase
from .models import TgUser, ProfileCard, Post, path_post_pic, path_prof_pic
from mixer.backend.django import mixer
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from PIL import Image
# Create your tests here.


class TestCabinet(TestCase):
    def setUp(self):
        image = io.BytesIO()
        Image.new("RGB", (1080, 1080)).save(image, "JPEG")
        image.seek(0)

        self.filename = "simple_image"
        self.file = SimpleUploadedFile(self.filename, image.getvalue())

        self.tg_user = mixer.blend(TgUser, telegram="qwerty")
        self.posts_count = 3
        self.posts = [mixer.blend(Post, user=self.tg_user, media=self.file)
                      for i in range(self.posts_count)]

    def test_telegram(self):
        tg_user = self.tg_user
        self.assertEqual(tg_user.telegram, "qwerty")
        self.assertEqual(tg_user.__str__(), tg_user.username)

    def test_profile_creation_single(self):
        profiles = ProfileCard.objects.all()
        self.assertEqual(1, len(profiles))

    def test_profile_creation(self):
        profile = ProfileCard.objects.get(user=self.tg_user)
        self.assertEqual(self.tg_user, profile.user)
        self.assertEqual(profile.__str__(), profile.name)

    def test_posts_creation(self):
        posts = Post.objects.filter(user=self.tg_user)
        self.assertEqual(self.posts_count, len(posts))
        self.assertEqual(posts[0].__str__(), posts[0].title)

    def test_path_post_pic(self):
        self.assertEqual(self.posts[0].media, path_post_pic(
            self.posts[0], self.filename))

    def test_path_prof_pic(self):
        profile = ProfileCard.objects.get(user=self.tg_user)
        profile.profile_pic = self.file
        profile.save()
        self.assertEqual(profile.profile_pic, path_prof_pic(
            profile, self.filename))
