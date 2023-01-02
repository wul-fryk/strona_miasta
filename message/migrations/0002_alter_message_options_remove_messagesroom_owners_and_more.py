# Generated by Django 4.1.4 on 2023-01-02 14:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('message', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-added']},
        ),
        migrations.RemoveField(
            model_name='messagesroom',
            name='owners',
        ),
        migrations.AddField(
            model_name='messagesroom',
            name='owner1',
            field=models.ManyToManyField(related_name='owner1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='messagesroom',
            name='owner2',
            field=models.ManyToManyField(related_name='owner2', to=settings.AUTH_USER_MODEL),
        ),
    ]