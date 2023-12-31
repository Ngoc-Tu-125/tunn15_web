# Generated by Django 4.2.5 on 2023-10-06 14:55

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0002_blogpost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='image_url',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(blank=True, help_text='Upload an image for the blog post.', null=True, upload_to='blog_images/'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='full_content',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
