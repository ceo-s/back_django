from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("login/", views.LoginUserView.as_view(), name="login"),
    path("logout/", views.logout_user, name="logout"),
]