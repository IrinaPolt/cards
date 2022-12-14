from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from .forms import CreationForm


User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('quizzes:index')
    template_name = 'users/signup.html'
