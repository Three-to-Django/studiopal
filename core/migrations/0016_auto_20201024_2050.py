# Generated by Django 3.1.2 on 2020-10-24 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_merge_20201024_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video_thumbnail',
            field=models.ImageField(blank=True, default='img/naurto_thumbsup.jpg', null=True, upload_to='media/img/'),
        ),
    ]
