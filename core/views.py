import os, json, uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.files import File
from .forms import InstructorForm, VideoForm, CommentsForm
from .models import Video, Comment
from users.models import User
from studiopal.settings import AZURE_STATIC_ROOT, MEDIA_URL

from moviepy.editor import *
from PIL import Image


@login_required
def video_upload(request):
    def create_video_thumbnail(video_obj):
        # video_path = f"{MEDIA_URL}" + f"{video_obj}"
        with VideoFileClip(video_obj.video.name, audio=False) as clip:
            duration = clip.duration
            max_duration = int(clip.duration) + 1
            print(max_duration)
            frame_at_second = 3
            thumbnail_frame = clip.get_frame(frame_at_second)
            video_thumbnail = Image.fromarray(thumbnail_frame)
            thumbnail_path = os.path.join(AZURE_STATIC_ROOT, f"{video}.jpg")
            video_thumbnail.save(thumbnail_path)
            clip.close()

            # create an ImageFile compatable with Django's ORM/Postgres

            try:
                thumbnail_buffer = open(thumbnail_path, "rb")
            except FileExistsError:
                raise Exception("thumbnail file not captured from video properly")

            thumbnail = File(thumbnail_buffer)

            video.video_thumbnail.save(f"{video}.jpg", thumbnail)

    if request.method == "POST":
        os.makedirs(AZURE_STATIC_ROOT, exist_ok=True)
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.creator = request.user
            video.save()
            create_video_thumbnail(video)
            return redirect("video_detail", video_pk=video.pk)
    form = VideoForm()
    return render(request, "studiopal/video_upload.html", {"form": form})


def video_detail(request, video_pk):
    video = Video.objects.get(id=video_pk)
    return render(request, "studiopal/video_detail.html", {"video": video})


def landing_page(request):
    videos = Video.objects.all()
    return render(request, "studiopal/landing_page.html", {"videos": videos})


@login_required
def add_comment(request, video_pk):
    video = get_object_or_404(Video, pk=video_pk)
    user = request.user
    if request.method == "POST":
        comment_json = json.loads(request.body)
        comment = comment_json["text"]
        new_comment = Comment(text=comment, author=user, video=video)
        new_comment.save()
        html = (
            f'<p class="comment-text">{new_comment.text}</p>'
            f'<p class="comment-author">by <span class="font-weight-bold">{user.username}</span>'
            f"</p>"
        )
    return JsonResponse({"html": html})


@login_required()
def add_studio_info(request, user_pk):
    user = get_object_or_404(User.objects.all(), pk=user_pk)
    if request.method == "POST":
        form = InstructorForm(data=request.POST, instance=user, files=request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect(to="studio_detail", user_pk=user.pk)
    else:
        form = InstructorForm(instance=user)
    return render(
        request, "studiopal/add_studio_info.html", {"form": form, "user": user}
    )


@login_required
def studio_detail(request, user_pk):
    user = get_object_or_404(User.objects.all(), pk=user_pk)
    return render(request, "studiopal/studio_detail.html", {"user": user})


def about(request):
    return render(request, "studiopal/about.html")


def search_instructors_videos(request):
    if request.method == "GET":
        query = request.GET.get("search")
        if query:
            videos = Video.objects.search().filter(search=query).distinct("pk")
        else:
            videos = None

    return render(
        request,
        "studiopal/search_results.html",
        {"videos": videos, "query": query or ""},
    )


def user_detail(request, user_pk):
    user = get_object_or_404(User.objects.all(), pk=user_pk)
    return render(request, "studiopal/user_detail.html", {"user": user})