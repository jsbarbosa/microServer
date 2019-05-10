from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(ModelForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('nombre', 'documento', 'institucion', 'direccion', 'ciudad', 'telefono')
        exclude = ('password', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
