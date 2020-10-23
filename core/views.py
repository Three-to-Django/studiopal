import os, json
from django.core.files import File
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from moviepy.editor import *
from PIL import Image

from .forms import InstructorForm, VideoForm, CommentsForm
from .models import Video, Comment, Preference
from users.models import User
from studiopal.settings import AZURE_STATIC_ROOT


@login_required
def video_upload(request):
    def create_video_thumbnail(video_obj):
        os.makedirs(AZURE_STATIC_ROOT, exist_ok=True)

        with VideoFileClip(video_obj.video.path, audio=False) as clip:
            fbs = clip.reader.fps
            nframes = clip.reader.nframes
            duration = clip.duration
            max_duration = int(clip.duration) + 1
            print(max_duration)
            frame_at_second = 3
            thumbnail_frame = clip.get_frame(frame_at_second)

            new_image_filepath = os.path.join(AZURE_STATIC_ROOT, f"{video_obj}.jpg")
            new_image = Image.fromarray(
                thumbnail_frame
            )  # convert numpy array into an image, save to storage.
            new_image.save(new_image_filepath)

            # saving to postgres
            try:
                thumbnail_buffer = open(new_image_filepath, "rb")
            except FileNotFoundError:
                raise Exception("Thumbnail byte stream failed to open properly")

            thumbnail = File(thumbnail_buffer)

            clip.close()
            video_obj.video_thumbnail.save(f"{video_obj}.jpg", thumbnail)

    if request.method == "POST":
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

@login_required
def video_preference(request, video_id, userpreference):
        
    if request.method == "POST":
        video = get_object_or_404(Video, id=video_id)

        obj=''

        valueobj=''

        try:
            obj= Preference.objects.get(user=request.user, video=video)

            valueobj= obj.value #value of userpreference


            valueobj= int(valueobj)

            userpreference= int(userpreference)
    
            if valueobj != userpreference:
                obj.delete()


                upref= Preference()
                upref.user= request.user

                upref.video= video

                upref.value= userpreference


                if userpreference == 1 and valueobj != 1:
                    video.likes += 1
                    video.dislikes -=1
                elif userpreference == 2 and valueobj != 2:
                    video.dislikes += 1
                    video.likes -= 1
                

                upref.save()

                video.save()
        
        
                context= {'video': video,
                    'video_id': video_id}

                return render (request, 'studiopal/video_preference.html', context)

            elif valueobj == userpreference:
                obj.delete()
        
                if userpreference == 1:
                    video.likes -= 1
                elif userpreference == 2:
                    video.dislikes -= 1

                video.save()

                context= {'video_id': video_id}

                return render (request, 'studiopal/video_preference.html', context)
                            
                    
    
            
        except Preference.DoesNotExist:
            upref= Preference()

            upref.user= request.user

            upref.post= video

            upref.value= userpreference

            userpreference= int(userpreference)

            if userpreference == 1:
                video.likes += 1
            elif userpreference == 2:
                video.dislikes +=1

            upref.save()

            video.save()                            


            context= {'video': video,
                'video_id': video_id}

            return render (request, 'studiopal/video_preference.html', context)


    else:
        video= get_object_or_404(Video, id=video_id)
        context= {'video': video,
                    'video_id': video_id}

        return render (request, 'studiopal/video_preference.html', context)
# def like(request, video_pk):
#     video = get_object_or_404(Video, id=video_pk)
#     newlike = Like.objects.create(user=request.user, video=video)
#     newlike.video_pk = video
#     return redirect("studiopal/user_detail.html",)

# def like(request, video_pk):
#     video = get_object_or_404(Video, pk=video_pk)
#     try:
#         selected_videos = video.liked.get(pk=request.POST['choice'])
#     except (KeyError, Video.DoesNotExist):
#         return render(request, 'studiopal/user_detail.html', {
#             'video': video,
#             'error_message': "you don't like anything.",
#         })
#     else:
#         selected_videos.like += 1
#         selected_videos.save()
#         return render(request, "studiopal/user_detail.html", {
#             'video': video,
#             'selected_videos': selected_videos