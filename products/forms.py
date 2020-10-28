from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = []
        for cat in categories:
            friendly_names.append((cat.id, cat.friendly_name))
        self.fields['category'].choices = friendly_names

        placeholders = {
            'category': 'Category',
            'name': 'Name',
            'detail': 'Detail',
            'description': 'Description',
            'size': 'Size (cl)',
            'proof': 'Proof',
            'price': 'Price',
        }

        for field in self.fields:
            if field != "image":
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].label = False
                self.fields[field].widget.attrs['class'] = 'user-profile-input'
