from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

from .managers import CustomUserManager


####################################################################################
# CUSTOM USER MODELS
####################################################################################
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


####################################################################################
# CONTACTS MODELS
####################################################################################
PLATFORM_CHOICES = (
    ('facebook', 'Facebook'),
    ('twitter', 'Twitter'),
    ('instagram', 'Instagram'),
    ('linkedin', 'LinkedIn'),
)

class SocialLink(models.Model):
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=200)

####################################################################################
# BLOG POST MODELS
####################################################################################
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
# TECH BLOG POST MODELS
####################################################################################
TECHBLOG_TYPE_CHOICES = (
    ('python', 'Python'),
    ('cpp', 'C++'),
    ('test', 'Test'),
    ('other', 'Other')
)

class TechBlogPost(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='techblog_images/', null=True, blank=True, help_text="Upload an image for the tech blog post.")
    date_published = models.DateField(default=timezone.now)
    body_snippet = models.TextField(default="Tech Blog")
    full_content = RichTextUploadingField(default="Tech Blog full content")
    slug = models.SlugField(unique=True)
    tech_type = models.CharField(max_length=50, choices=TECHBLOG_TYPE_CHOICES, help_text="Type of the technical blog post.")

    def __str__(self):
        return self.title



####################################################################################
# HOME PAGE CONTENT MODELS
####################################################################################
class HomePageContent(models.Model):
    section_name = models.CharField(max_length=255)  # 'intro', 'delivery', 'success'
    title = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
