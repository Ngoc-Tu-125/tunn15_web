import os
from django.conf import settings
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from PIL import Image
from django.utils.html import format_html

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

    def __str__(self):
        return f"{self.name}"

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
    optimized_image = ImageSpecField(source='image',
                                      processors=[ResizeToFill(600, 400)],
                                      format='JPEG',
                                      options={'quality': 85})

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        # Delete the image file from the filesystem
        if self.image and os.path.isfile(os.path.join(settings.MEDIA_ROOT, self.image.path)):
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
        super(BlogPost, self).delete(*args, **kwargs)


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
    optimized_image = ImageSpecField(source='image',
                                      processors=[ResizeToFill(600, 400)],
                                      format='JPEG',
                                      options={'quality': 85})


    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        # Delete the image file from the filesystem
        if self.image and os.path.isfile(os.path.join(settings.MEDIA_ROOT, self.image.path)):
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
        super(TechBlogPost, self).delete(*args, **kwargs)


####################################################################################
# EBOOK PICTURES MODELS
####################################################################################
class Card(models.Model):
    image = models.ImageField(upload_to='cards/')
    title = models.CharField(max_length=200)
    short_intro = models.TextField()
    optimized_image = ImageSpecField(source='image',
                                      processors=[ResizeToFill(400, 400)],
                                      format='JPEG',
                                      options={'quality': 85})
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Open the image using Pillow:
        img = Image.open(self.image.path)

        # Resize the image if it's too large:
        max_width = 1920
        max_height = 1280
        if img.width > max_width or img.height > max_height:
            base_width = max_width
            w_percent = base_width / float(img.width)
            h_size = int(float(img.height) * float(w_percent))
            img = img.resize((base_width, h_size), Image.LANCZOS)

        # Save the optimized image:
        img.save(self.image.path, format='JPEG', quality=85)  # Quality level can be adjusted based on your needs

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the image file from the filesystem
        if self.image and os.path.isfile(os.path.join(settings.MEDIA_ROOT, self.image.path)):
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
        super(Card, self).delete(*args, **kwargs)

    class Meta:
        ordering = ['order']


class ImageDetail(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='details/')
    caption = models.CharField(max_length=300)
    optimized_image = ImageSpecField(source='image',
                                      processors=[ResizeToFill(400, 400)],
                                      format='JPEG',
                                      options={'quality': 85})
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.caption

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Open the image using Pillow:
        img = Image.open(self.image.path)

        # Resize the image if it's too large:
        max_width = 1920
        max_height = 1280
        if img.width > max_width or img.height > max_height:
            base_width = max_width
            w_percent = base_width / float(img.width)
            h_size = int(float(img.height) * float(w_percent))
            img = img.resize((base_width, h_size), Image.LANCZOS)

        # Save the optimized image:
        img.save(self.image.path, format='JPEG', quality=85)  # Quality level can be adjusted based on your needs

        super().save(*args, **kwargs)

    def display_image(self):
        return format_html('<img src="{}" width="50" height="50" />', self.image.url)
    display_image.short_description = 'Image'

    def delete(self, *args, **kwargs):
        # Delete the image file from the filesystem
        if self.image and os.path.isfile(os.path.join(settings.MEDIA_ROOT, self.image.path)):
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
        super(ImageDetail, self).delete(*args, **kwargs)

    class Meta:
        ordering = ['order']

####################################################################################
# HOME PAGE CONTENT MODELS
####################################################################################
class HomePageContent(models.Model):
    section_name = models.CharField(max_length=255)  # 'intro', 'delivery', 'success'
    title = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    optimized_image = ImageSpecField(source='image',
                                      processors=[ResizeToFill(500, 400)],
                                      format='JPEG',
                                      options={'quality': 85})

    def delete(self, *args, **kwargs):
        # Delete the image file from the filesystem
        if self.image and os.path.isfile(os.path.join(settings.MEDIA_ROOT, self.image.path)):
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
        super(HomePageContent, self).delete(*args, **kwargs)
