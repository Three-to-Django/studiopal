# Generated by Django 3.1.2 on 2020-10-22 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20201022_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='liked',
            field=models.ManyToManyField(related_name='videos', to='core.Like'),
        ),
    ]