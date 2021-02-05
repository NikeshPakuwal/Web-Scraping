from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import ScrapWeb

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']

class ScrapForm(forms.ModelForm):
    class Meta:
        model = ScrapWeb
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
