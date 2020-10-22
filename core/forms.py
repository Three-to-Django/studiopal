from django import forms
from .models import Video, Comment, User


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = [
            "title",
            "video",
            "description",
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
