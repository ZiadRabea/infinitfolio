# Generated by Django 4.2 on 2023-04-28 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_heading_element_remove_image_element_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paragraph',
            name='src',
        ),
        migrations.AddField(
            model_name='paragraph',
            name='text',
            field=models.TextField(default=1, max_length=10000),
            preserve_default=False,
        ),
    ]
