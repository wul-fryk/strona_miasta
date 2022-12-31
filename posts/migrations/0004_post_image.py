# Generated by Django 4.1.4 on 2022-12-30 17:37

from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_post_options_like_dislike'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=posts.models.get_image_filepath),
        ),
    ]