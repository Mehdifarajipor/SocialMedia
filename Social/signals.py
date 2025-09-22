from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver
from .models import Post
from django.core.mail import send_mail
from  django.conf import settings

@receiver(m2m_changed, sender=Post.likes.through)
def user_like_changed(sender, instance,**kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()


@receiver(post_delete, sender=Post)
def send_delete_email_to_user(sender, instance,**kwargs):
    user = instance.author
    subject = 'Delete your post'
    message = f'we deleted your post with id {instance.id}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])