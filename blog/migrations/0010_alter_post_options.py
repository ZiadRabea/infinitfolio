# Generated by Django 5.0.7 on 2024-11-25 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_post_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-date']},
        ),
    ]
