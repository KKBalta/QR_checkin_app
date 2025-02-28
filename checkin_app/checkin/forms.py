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
    country_code = forms.CharField(widget=forms.HiddenInput(), required=True)
    
    def clean(self):
        cleaned_data = super().clean()
        country_code = cleaned_data.get('country_code')
        phone_number = cleaned_data.get('phone_number')
        
        if phone_number and country_code:
            # Combine country code and phone number
            full_phone = f"{country_code}{phone_number}"
            cleaned_data['phone_number'] = full_phone
        
        return cleaned_data

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'email', 'phone_number', 'country_code']


