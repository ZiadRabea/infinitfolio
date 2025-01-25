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

    def __init__(self, *args, **kwargs):
        store = kwargs.pop('store', None)
        print(store)
        super(AddProduct, self).__init__(*args, **kwargs)
        self.fields['cls'].queryset = Category.objects.filter(store=store)

class AddCategory(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

