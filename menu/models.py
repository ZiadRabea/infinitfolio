from django.db import models
from Accounts.models import Profile
# Create your models here.


class Menu(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    qr = models.ImageField(null=True, blank=True, upload_to="images")


class MenuProduct(models.Model):
    product = models.CharField(max_length=200)
    price = models.IntegerField()
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)


class QrRequest(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
