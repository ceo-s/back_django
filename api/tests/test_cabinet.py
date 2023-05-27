from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from mixer.backend.django import mixer
from cabinet.models import TgUser, Post
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from PIL import Image
# Create your tests here.


class TestCoachingViews(APITestCase):

    def setUp(self):
        self.user = mixer.blend(TgUser, username="alex", password="qwerty")
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    # def test_user_registration(self):
    #     # a = self.client.post("token-auth/users/", data={
    #     #  "username": "alex2", "password": "qwerty", "telegram": "alex2"})
    #     a = self.client.get(reverse("registration"))
    #     print("wth", a)

    def test_user_login(self):
        token = Token.objects.get(user__username=self.user.username)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token' + token.key)
        self.assertEqual(
            client._credentials["HTTP_AUTHORIZATION"], f"Token{token}")

    def test_profile_retrieve(self):
        response = self.client.get(
            reverse("profile-detail", kwargs={"pk": "my_profile"}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user"]["id"], self.user.id)

    def test_post_invalid_create(self):
        image = io.BytesIO()
        Image.new("RGB", (1080, 1080)).save(image, "jpeg")
        image.seek(0)
        file = SimpleUploadedFile("simple_image.jpeg", image.getvalue())
        self.client.logout()

        response = self.client.post(
            reverse("post-list"), data={"title": "Title", "content": "Content", "media": file})

        self.assertEqual(response.status_code, 400)

    def test_post_valid_create(self):
        image = io.BytesIO()
        Image.new("RGB", (1080, 1080)).save(image, "jpeg")
        image.seek(0)
        file = SimpleUploadedFile("simple_image.jpeg", image.getvalue())

        response = self.client.post(
            reverse("post-list"), data={"title": "Title", "content": "Content", "media": file})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["user"], self.user.id)

    def test_post_list(self):
        posts = [mixer.blend(Post, user=self.user) for i in range(3)]
        response = self.client.get(reverse("post-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(posts))
