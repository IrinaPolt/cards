from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm

User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('cards:index')
    template_name = 'users/signup.html'
