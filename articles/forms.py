from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import Posts
from django.contrib.auth import authenticate
from django.contrib import messages

class PostContentForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields=['title','text','picture','title_url','created_date','published_date','category']



