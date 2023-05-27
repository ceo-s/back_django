from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login

from . import forms

# Create your views here.


class RegistrationView(CreateView):
    form_class = forms.RegisterForm
    # model = User
    template_name = "authorization/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(to="authorization", slug=user.username)
    

class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = "authorization/login.html"
    
    def get_success_url(self):
        return reverse_lazy("users")
    
def logout_user(request):
    logout(request)
    return redirect(to="users")