# Generated by Django 4.2.5 on 2023-10-15 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0010_alter_imagedetail_options_imagedetail_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='card',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
