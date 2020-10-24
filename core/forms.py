import os
from django import forms
from django.core.files.storage import default_storage
from studiopal.settings import AZURE_STATIC_ROOT
from .models import Video, Comment, User
from moviepy.editor import *
from PIL import Image


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
