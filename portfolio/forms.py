from django.forms import ModelForm
from.models import *


class CreateWebsite(ModelForm):
    class Meta:
        model = Website
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
        exclude = ['unique_name', 'full_name', 'age']


