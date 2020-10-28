import os
from django import forms
from django.core.files.storage import default_storage
from studiopal.settings import AZURE_STATIC_ROOT
from .models import Video, Comment, User
from moviepy.editor import *
from PIL import Image
from django.contrib.auth.forms import UserCreationForm
from registration.forms import RegistrationForm


class VideoForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput())
    description = forms.CharField(widget=forms.Textarea())
    video = forms.FileField(required=True, widget=forms.FileInput())

    class Meta:
        model = Video
        fields = [
            "title",
            "description",
            "video",
        ]


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class InstructorForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "studio_name",
            "profile_photo",
            "bio",
            "paypal_donation_url",
        ]
        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {
            "profile_photo",
            "user_bio",
        }

class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(max_length=55)

    class Meta:
        model= User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]