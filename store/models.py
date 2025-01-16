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

    def __str__(self):
        return f"{self.title} | {self.description}"

class Product(models.Model):
    name = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to="cover_image", storage=MediaCloudinaryStorage)
    original_price = models.IntegerField(null=True, blank=True)
    affiliate_link = models.CharField(max_length=1000, null=True, blank=True)
    affiliate_product = models.BooleanField(default=False)
    description = models.TextField(max_length=1000)
    price = models.IntegerField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.name} | {self.store}"
