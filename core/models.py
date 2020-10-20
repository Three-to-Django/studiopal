from django.db import models


# Create your models here.

from imagekit.models import ImageSpecField
from taggit.managers import TaggableManager
from users.models import User

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=511)
    description = models.TextField(max_length=5000, blank=True)
    creator = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="videos"
    )
    video = models.FileField(upload_to="media/")
    # thumbnail
    upvoted = models.IntegerField(default=0)
    tags = TaggableManager()

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


# class Gallery(models.Model):
#     title = models.CharField(max_length=500)
#     owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='galleries', blank=True)
#     tags = TaggableManager()
#     def __str__(self):
#         return self.title
