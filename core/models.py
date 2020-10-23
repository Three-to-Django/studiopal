from django.db import models
from django.contrib.postgres.search import SearchVector


# Create your models here.

from imagekit.models import ImageSpecField
from taggit.managers import TaggableManager
from users.models import User


class VideoQuerySet(models.QuerySet):
    def search(self):
        video_results = self.annotate(
            search=SearchVector(
                "creator__studio_name", "creator__bio", "title", "description"
            )
        )
        return video_results


# Create your models here.
class Video(models.Model):
    objects = VideoQuerySet.as_manager()
    title = models.CharField(max_length=511)
    description = models.TextField(max_length=5000, blank=True)
    creator = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="videos"
    )
    video = models.FileField(upload_to="media/")
    video_thumbnail = models.ImageField(
        upload_to="media/img/", default="img/naurto_thumbsup.jpg", null=True, blank=True
    )
    tags = TaggableManager()
    liked = models.ManyToManyField(to="like", related_name="videos")
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(max_length=5000)
    pub_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="comments"
    )
    video = models.ForeignKey(
        to=Video, on_delete=models.CASCADE, related_name="comments"
    )


class Like(models.Model):
    count = models.IntegerField(default=True, blank=True, null=True)
    user = models.ForeignKey(
        to=User, related_name="likes", on_delete=models.CASCADE, null=True
    )
