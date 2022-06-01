from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils import timezone

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, verbose_name='Nickname')
    is_staff = models.BooleanField(default=False, verbose_name='Is staff')
    is_superuser = models.BooleanField(default=False, verbose_name='Admin')
    is_banned = models.BooleanField(default=False, verbose_name='Is banned')
    last_login = models.DateTimeField(default=None, null=True, verbose_name='Las time login')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Joined')

    def __str__(self):
        return self.username


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    video = models.ForeignKey('Video', on_delete=models.CASCADE, verbose_name='Video')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Liked')

    def __str__(self):
        return self.user.username + ': ' + self.video.title[:10] + '...'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    video = models.ForeignKey('Video', on_delete=models.CASCADE, verbose_name='Video')
    text = models.TextField(max_length=500, verbose_name='Comment')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Liked')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')

    def __str__(self):
        return self.user.username + ': ' + self.text[:10] + '...' + ': ' + self.video.title[:10] + '...'

class Video(models.Model):
    title = models.CharField(max_length=150, verbose_name='Video name')
    content = models.FileField(upload_to='videos/', null=True, validators=[FileExtensionValidator(allowed_extensions=['mov','avi','mp4','webm','mkv'])], verbose_name="Video content")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_by', verbose_name='Uploaded by')
    subscribers = models.ManyToManyField(User, related_name='subscribers', verbose_name='Subscribers')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Uploaded')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')

    def get_likes(self):
        return Like.objects.filter(video=self.pk).count()

    def get_comments(self):
        return Comment.objects.filter(video=self.pk)

    def __str__(self):
        return self.title