from django.forms import ModelForm
from.models import *


class CreateWebsite(ModelForm):
    class Meta:
        model = Website
        fields = '__all__'

class SubScribe(ModelForm):
    class Meta:
        model = newsletter
        fields = '__all__'

class AddSkill(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['website']


class AddProject(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['website']


class AddCertificate(ModelForm):
    class Meta:
        model = Certificate
        fields = '__all__'
        exclude = ['website']


class AddExperience(ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'
        exclude = ['website']


class EditWebsite(ModelForm):
    class Meta:
        model = Website
        fields = '__all__'
        exclude = ['unique_name', 'full_name', 'age', 'is_active']


class CreateCommnunityPost(ModelForm):
    class Meta: 
        model = Post
        fields = "__all__"
        exclude = ["profile", ]

class AddComment(ModelForm):
    class Meta: 
        model = Comment
        fields = "__all__"
        exclude = ["profile", "post"]