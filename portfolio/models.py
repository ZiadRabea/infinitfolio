from django.db import models
from Accounts.models import Profile
from cloudinary_storage.storage import MediaCloudinaryStorage
# Create your models here.


class Website(models.Model):
    unique_name = models.SlugField(max_length=500, unique=True)
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, blank=True)
    is_active = models.BooleanField(default=False)
    cv_url = models.URLField(null=True, blank=True)
    full_name = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to="profile_pictures", storage=MediaCloudinaryStorage)
    current_job = models.CharField(max_length=500)
    about = models.TextField(max_length=2000)
    email = models.EmailField()
    age = models.IntegerField()
    analytics = models.CharField(max_length=200, null=True, blank=True)
    adsense = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
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
    cert = models.ImageField(upload_to="Certificates", storage=MediaCloudinaryStorage)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)


class Experience(models.Model):
    job = models.CharField(max_length=100)
    years = models.IntegerField()
    about = models.TextField(max_length=2000)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)


class newsletter(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

class Post(models.Model):
    profile = models.ForeignKey(Website, on_delete=models.CASCADE, null=True, blank=True, related_name="post_profile")
    text = models.TextField(max_length=10000, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Website, blank=True, related_name="likes")
    dislikes = models.ManyToManyField(Website, blank=True, related_name="dislikes")
    image = models.ImageField(upload_to="posts", storage=MediaCloudinaryStorage, null="true", blank="true")
    
    class Meta:
        ordering = ["-date"]
    
    def __str__(self):
        return f"{self.text}"[:30] + " ..." if len(self.text) > 10 else self.text
    
class Comment(models.Model):
    profile = models.ForeignKey(Website, on_delete=models.CASCADE, null=True, blank=True, related_name="comment_profile")
    text = models.TextField(max_length=10000)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Website, blank=True, related_name="comment_likes")
    dislikes = models.ManyToManyField(Website, blank=True, related_name="comment_dislikes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ["-date"]
    
    def __str__(self):
        return f"{self.text}"[:30] + " ..." if len(self.text) > 10 else self.text

class Notification(models.Model):
    sender = models.ForeignKey(Website, on_delete=models.CASCADE, related_name="sender")
    content = models.TextField(max_length=1000)
    url = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    receiver = models.ForeignKey(Website, on_delete=models.CASCADE, related_name="receiver")
    
    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.content} | {str(self.receiver.full_name)}"
    
