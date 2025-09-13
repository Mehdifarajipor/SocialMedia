from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from taggit.managers import TaggableManager

# Create your models here.


class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    job = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    photo = models.ImageField(upload_to='users_images/', null=True, blank=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('Social:post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.author.username

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]