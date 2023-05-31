from django.forms import ModelForm
from.models import *


class CreateBlog(ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        exclude = ['user', 'published']


class AddPost(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['blog']


class AddHeading(ModelForm):
    class Meta:
        model = Heading
        fields = '__all__'


class AddParagraph(ModelForm):
    class Meta:
        model = Paragraph
        fields = '__all__'


class AddImage(ModelForm):
    class Meta:
        model = Image
        fields = '__all__'


class AddLink(ModelForm):
    class Meta:
        model = Link
        fields = '__all__'


class AddList(ModelForm):
    class Meta:
        model = List
        fields = '__all__'


class AddItem(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        exclude = ['list']


class AddFrame(ModelForm):
    class Meta:
        model = Iframe
        fields = '__all__'
