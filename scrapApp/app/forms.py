from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import widgets
from .models import ScrapWeb, ScrapData, StoreJsonData

from django_countries.widgets import CountrySelectWidget


class AuthUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name", "email", "is_active", "is_staff", "is_superuser", "user_permissions"]
    
    def __init__(self, *args, **kwargs):
        super(AuthUser, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-group col'

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


class CountryForm(forms.ModelForm):
    class Meta:
        model = ScrapData
        fields = ('country',)
        widgets = {'country': CountrySelectWidget()}


class JsonDataStore(forms.ModelForm):
    children = forms.MultipleChoiceField(
        choices= ['children', 'images', 'related_searches', 'related_questions', 'organic_results', 'books', 'profiles', 'people_also_search_for', 'known_attributes']
    )
    class Meta:
        model = StoreJsonData
        fields = '__all__'