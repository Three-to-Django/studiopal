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

    # def save(self, commit=True):
    #     video = super(VideoForm, self).save(commit=False)
    #     title = self.cleaned_data.get("title")
    #     description = self.cleaned_data.get("description")
    #     video = self.cleaned_data.get("video")
    #     with VideoFileClip(video.path, audio=False) as clip:
    #         duration = clip.duration
    #         max_duration = int(clip.duration) + 1
    #         print(max_duration)
    #         frame_at_second = 3
    #         thumbnail_frame = clip.get_frame(frame_at_second)
    #         video_thumbnail = Image.fromarray(thumbnail_frame)
    #         thumbnail_path = os.path.join(AZURE_STATIC_ROOT, f"{video}.jpg")
    #         video_thumbnail.save(thumbnail_path)
    #         clip.close()

    #         # create an ImageFile compatable with Django's ORM/Postgres

    #         try:
    #             thumbnail_buffer = open(thumbnail_path, "rb")
    #         except FileExistsError:
    #             raise Exception("thumbnail file not captured from video properly")

    #         thumbnail = File(thumbnail_buffer)

    #         video.video_thumbnail.save(f"{video}.jpg", thumbnail)

    #     if video.commit:
    #         video.save()

    #     return video


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
