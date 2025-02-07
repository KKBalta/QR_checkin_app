from django import forms
from .models import Workplace
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class WorkplaceForm(forms.ModelForm):
    class Meta:
        model = Workplace
        fields = ['name', 'location', 'latitude', 'longitude']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()  # Use the custom user model
        fields = ['username', 'password1', 'password2', 'email']


