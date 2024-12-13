from django import forms
from.models import MenuProduct


class MProduct(forms.ModelForm):
    class Meta:
        model = MenuProduct
        fields = "__all__"
        exclude = ["menu", ]
