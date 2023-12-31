# Generated by Django 4.2.5 on 2023-10-07 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0005_alter_homepageintrocontent_content_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=255)),
                ('title', models.TextField(blank=True, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
        migrations.DeleteModel(
            name='HomePageIntroContent',
        ),
    ]
