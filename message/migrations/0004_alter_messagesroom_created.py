# Generated by Django 4.1.4 on 2023-01-03 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0003_remove_messagesroom_owner1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagesroom',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
