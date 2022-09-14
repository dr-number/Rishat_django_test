from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
 
class RegistrationForm(UserCreationForm):
    description = models.CharField(max_length=255)
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )
        labels = {'description': 'Description'}


class AuthorizationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', )