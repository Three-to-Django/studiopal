# Generated by Django 3.1.2 on 2020-10-15 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_user_bio2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='bio2',
        ),
    ]
