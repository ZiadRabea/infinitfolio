# Generated by Django 5.0.7 on 2024-12-23 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_blog_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='type',
            field=models.CharField(choices=[('Tech', 'Tech'), ('Lifestyle', 'Lifestyle '), ('Food', 'Food'), ('Personal', 'Personal'), ('Science', 'Science'), ('YouTuber', 'YouTuber'), ('Educational', 'Educational'), ('School', 'School')], max_length=100),
        ),
    ]
