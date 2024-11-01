from django.db import models
from Accounts.models import Profile
from cloudinary_storage.storage import MediaCloudinaryStorage
# Create your models here.


class Blog(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    choices = (
                ("Science & Tech", "Science & Tech"), ("Lifestyle", "Lifestyle "),
                ("Food", "Food"), ("Personal", "Personal")
               )
    type = models.CharField(choices=choices, max_length=100)
    name = models.SlugField(max_length=500)
    published = models.BooleanField(default=False)


class Element(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    choices = (
                ("heading", "heading"), ("list", "list"),
                ("image", "image"), ("link", "link"),
                ("paragraph", "paragraph"), ("line", "line"),
                ("frame", "frame")
    )
    type = models.CharField(choices=choices, max_length=10)
    heading = models.ForeignKey("Heading", on_delete=models.CASCADE, null=True, blank=True)
    list = models.ForeignKey("List", on_delete=models.CASCADE, null=True, blank=True)
    link = models.ForeignKey("Link", on_delete=models.CASCADE, null=True, blank=True)
    image = models.ForeignKey("Image", on_delete=models.CASCADE, null=True, blank=True)
    p = models.ForeignKey("Paragraph", on_delete=models.CASCADE, null=True, blank=True)
    frame = models.ForeignKey("Iframe", on_delete=models.CASCADE, null=True, blank=True)


class Post(models.Model):
    title = models.CharField(max_length=200)
    published = models.BooleanField(default=False)
    cover_img = models.ImageField(upload_to="cover_images", storage=MediaCloudinaryStorage)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)


class Heading(models.Model):
    text = models.CharField(max_length=500)


class Link(models.Model):
    text = models.CharField(max_length=500)
    url = models.URLField()


class Image(models.Model):
    src = models.URLField()


class Paragraph(models.Model):
    text = models.TextField(max_length=10000)


class List(models.Model):
    types = (
        ("ul", "ul"),
        ("ol", "ol")
    )
    type = models.CharField(max_length=2, choices=types)


class Iframe(models.Model):
    src = models.URLField()


class Item(models.Model):
    text = models.CharField(max_length=100)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
