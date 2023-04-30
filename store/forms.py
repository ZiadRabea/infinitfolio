from django.forms import ModelForm
from.models import *


class CreateStore(ModelForm):
    class Meta:
        model = Store
        fields = '__all__'
        exclude = ["user", "approved", "published"]


class AddProduct(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ["store", "approved"]
