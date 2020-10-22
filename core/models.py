from django.db import models
from django.contrib.postgres.search import SearchVector
from imagekit.models import ImageSpecField
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify

from users.models import User

# Create your models here.




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
    # url = models.slugField(max_length=300)
    title = models.CharField(max_length=511)
    description = models.TextField(max_length=5000, blank=True)
    creator = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="videos"
    )
    video = models.FileField(upload_to="media/")
    # thumbnail
    tags = TaggableManager()
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.url = slugify(self.title)
        super(Video, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(max_length=5000)
    pub_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="comments"
    )
    video = models.ForeignKey(
        to=Video, on_delete=models.CASCADE, related_name="comments")
    

class Preference(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    video = models.ForeignKey(to=Video, on_delete=models.CASCADE)
    value = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return str(self.user) + ':' + str(self.video) +':' + str(self.value)

    class Meta:
       unique_together = ("user", "video", "value")