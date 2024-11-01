from django.db import models
from Accounts.models import Profile
from cloudinary_storage.storage import MediaCloudinaryStorage
# Create your models here.


class Store(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    name = models.SlugField()
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=1000)
    phone = models.CharField(max_length=12)
    email = models.EmailField()
    approved = models.BooleanField(default=False)


class Product(models.Model):
    name = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)
    cover_image = models.ImageField(upload_to="cover_image", storage=MediaCloudinaryStorage)
    description = models.TextField(max_length=1000)
    price = models.IntegerField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

