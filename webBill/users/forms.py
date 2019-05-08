from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(ModelForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('nombre', 'documento', 'institucion', 'direccion', 'ciudad', 'telefono')
        exclude = ('password', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)
