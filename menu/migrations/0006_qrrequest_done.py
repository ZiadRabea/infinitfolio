# Generated by Django 4.2 on 2023-06-07 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_qrrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='qrrequest',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
