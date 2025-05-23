# Generated by Django 4.2.14 on 2025-03-04 08:49

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0014_alter_notification_options_notification_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank='true', null='true', storage=cloudinary_storage.storage.MediaCloudinaryStorage, upload_to='posts'),
        ),
        migrations.AlterField(
            model_name='website',
            name='cv_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
