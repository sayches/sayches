from django.dispatch import receiver
from posts.views import delete_post
from .models import Post

@receiver(delete_post, sender=Post)
def delete_media_from_s3(sender, instance, using, **kwargs):
    instance.media.delete(save=False)
