from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import User, Video, Comment
from .forms import InstructorForm, VideoForm, CommentsForm
import json
from django.contrib.auth.decorators import login_required


@login_required
def video_upload(request):
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.creator = request.user
            video.save()
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
def add_instructor_info(request, user_pk):
    user = get_object_or_404(User.objects.all(), pk=user_pk)
    if request.method == "POST":
        form = InstructorForm(data=request.POST, instance=user, files=request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect(to="instructor_detail", user_pk=user.pk)
    else:
        form = InstructorForm(instance=user)
    return render(
        request, "studiopal/add_instructor_info.html", {"form": form, "user": user}
    )


@login_required
def instructor_detail(request, user_pk):
    user = get_object_or_404(User.objects.all(), pk=user_pk)
    return render(request, "studiopal/instructor_detail.html", {"user": user})


def about(request):
    return render(request, "studiopal/about.html")
