from django.contrib import admin
from.models import Website, Skill, Experience, Project, Certificate, Post, Comment, Notification
# Register your models here.

admin.site.register(Website)

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Skill)
admin.site.register(Certificate)
admin.site.register(Project)
admin.site.register(Experience)
admin.site.register(Notification)