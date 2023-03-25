from django import forms 
from django.contrib.auth import authenticate, get_user_model
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_no = forms.CharField(max_length = 20, required=True)
    first_name = forms.CharField(max_length = 20, required=True)
    last_name = forms.CharField(max_length = 20, required=True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'phone_no', 'password1', 'password2']