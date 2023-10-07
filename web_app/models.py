from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True, help_text="Upload an image for the blog post.")
    date_published = models.DateField()
    body_snippet = models.TextField()
    full_content = RichTextUploadingField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


####################################################################################
# HOME PAGE CONTENT MODELS
####################################################################################
class HomePageContent(models.Model):
    section_name = models.CharField(max_length=255)  # 'intro', 'delivery', 'success-story'
    title = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
