from django import forms

from . import models

class ProductForm(forms.Form):
    product = forms.ModelChoiceField(models.Player.objects, label='商品',
                                     empty_label='選択してください', to_field_name='code')