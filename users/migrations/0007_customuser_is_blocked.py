# Generated by Django 4.1.4 on 2023-06-02 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_gestor_is_staff_customuser_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_blocked',
            field=models.BooleanField(default=False, verbose_name='blocked'),
        ),
    ]
