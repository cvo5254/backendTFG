# Generated by Django 4.1.4 on 2023-05-10 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emergencies', '0003_emergency_reporter'),
    ]

    operations = [
        migrations.AddField(
            model_name='emergency',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]
