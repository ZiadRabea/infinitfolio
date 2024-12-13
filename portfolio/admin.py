from django.contrib import admin
from.models import Website, Skill, Experience, Project, Certificate
# Register your models here.

admin.site.register(Website)
admin.site.register(Skill)
admin.site.register(Certificate)
admin.site.register(Project)
admin.site.register(Experience)