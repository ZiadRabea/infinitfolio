from django.db import models
from Accounts.models import Profile
import datetime
from cloudinary_storage.storage import MediaCloudinaryStorage

# Create your models here.


class Store(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    name = models.SlugField()
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=1000)
    amazon_affiliate_id = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    approved = models.BooleanField(default=False)
    logo = models.ImageField(upload_to="store_logos", storage=MediaCloudinaryStorage, null=True)
    app = models.CharField(max_length=1000, null=True, blank=True)
    template = models.ForeignKey('Template', null=True, blank=True, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.title} | {self.description}"

class Product(models.Model):
    name = models.CharField(max_length=1000)
    approved = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to="cover_image", storage=MediaCloudinaryStorage)
    original_price = models.CharField(max_length=9, null=True, blank=True)
    affiliate_link = models.CharField(max_length=5000, null=True, blank=True)
    affiliate_product = models.BooleanField(default=False)
    savers = models.ManyToManyField(Profile, blank=True, related_name="savers")
    description = models.TextField(max_length=5000)
    price = models.CharField(max_length=9)
    cls = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    views = models.IntegerField(default=0, null=True, blank=True)

    def increment_views(self):
        """Increment views for this product"""
        self.views += 1
        self.store.views += 1
        self.save()
        self.store.save()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.name} | {self.store}"

class Chart(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    views = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Override save to ensure only one record per month for each store."""
        if self.id is None:
            # Remove existing records for the same month before saving the new one
            Chart.objects.filter(store=self.store, date__year=datetime.datetime.now().year, date__month=datetime.datetime.now().month).delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.store.name} - {self.date.strftime('%b %Y')}"

class Template(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to="templates", storage=MediaCloudinaryStorage)
    gif = models.ImageField(upload_to="tempgifs", storage=MediaCloudinaryStorage)
    url = models.URLField(max_length=1000)
    template = models.CharField(max_length=1000)

    class Meta:
        ordering = ['-date']
    

    def __str__(self):
        return f"{self.template} | {self.url}"

class Category(models.Model):
    title = models.CharField(max_length=200)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"