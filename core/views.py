from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import User, Video, Comment
from .forms import InstructorForm, VideoForm, CommentsForm
import json

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

# def add_comment(request, video_pk):
#     video = get_object_or_404(Video, pk=video_pk)
#     if request.method == "POST":
#         form = VideoForm()
#         form = CommentsForm(data=request.POST)
#         if form.is_valid():
#             comments = form.save(commit=False)
#             comments.author = request.user
#             comments.video = video
#             comments.save()
#             return redirect(to="video_detail", video_pk=video_pk)
#     return render(
#         request, "studiopal/video_detail.html", {"video": video,"form": form,}
#     )

# This view needs to accept a POST but does not need to handle a GET, and you don't need
# to use a Django form object. The job of this view is to handle the request, take the data
# from the POST body, and use it to create a new Comment object and save it to the database.
# Then, return a response with that same successfully saved data. When the response comes back
# You'll need to use the data to update the DOM
def add_comment(request, video_pk):
    print("ADD COMMENT VIEW CALLED")
    video = get_object_or_404(Video, pk=video_pk)
    user = request.user
    if request.method == "POST":
        comment_json = json.loads(request.body)
        comment = comment_json["text"]
        new_comment = Comment(text=comment, author=user, video=video)
        new_comment.save()
        html = f'<p class="comment-text">{new_comment.text}</p>'  \
        f'<p class="comment_author">by <span class="font-weight-bold">{user.username}</span>' \
        f'</p>'
    return JsonResponse({"html": html})



def delete_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == "POST":
        comment.delete()
        return redirect(to="landing_page")
    return render(request, "studiopal/delete_comment.html", {"comment": comment})


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


def instructor_detail(request, user_pk):
    user = get_object_or_404(User.objects.all(), pk=user_pk)
    return render(request, "studiopal/instructor_detail.html", {"user": user})



