# Generated by Django 5.0.7 on 2024-11-24 06:11

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_qrrequest_done'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='qr',
            field=models.ImageField(blank=True, null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage, upload_to='images'),
        ),
    ]
