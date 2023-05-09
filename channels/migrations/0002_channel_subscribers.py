# Generated by Django 4.1.4 on 2023-05-09 15:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('channels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='subscribers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
