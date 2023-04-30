from django.db import models
from Accounts.models import Profile
# Create your models here.


class Website(models.Model):
    unique_name = models.SlugField(max_length=500)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
    is_active = models.BooleanField(default=False)
    cv_url = models.URLField()
    full_name = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to="profile_pictures")
    current_job = models.CharField(max_length=500)
    about = models.TextField(max_length=2000)
    email = models.EmailField()
    age = models.IntegerField()
    analytics = models.CharField(max_length=200, null=True, blank=True)
    adsense = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=13)
    fb = models.URLField(null=True, blank=True)
    insta = models.URLField(blank=True, null=True)
    tele = models.URLField(blank=True, null=True)
    wp = models.URLField(null=True, blank=True)


class Skill(models.Model):
    skill = models.CharField(max_length=100)
    mastery = models.IntegerField()
    website = models.ForeignKey(Website, on_delete=models.CASCADE)


class Project(models.Model):
    title = models.CharField(max_length=100)
    about = models.TextField(max_length=2000)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)


class Certificate(models.Model):
    cert = models.ImageField(upload_to="Certificates")
    website = models.ForeignKey(Website, on_delete=models.CASCADE)


class Experience(models.Model):
    job = models.CharField(max_length=100)
    years = models.IntegerField()
    about = models.TextField(max_length=2000)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
