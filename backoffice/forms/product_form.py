from django import forms

from catalog.models import Product


class ProductForm(forms.ModelForm):
    """Класс для валидации формы создания и изменения продукта"""

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'preview']
