# Generated by Django 4.2 on 2023-06-06 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_alter_menu_qr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='qr',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
