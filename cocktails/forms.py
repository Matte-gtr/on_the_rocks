from django import forms
from .models import Cocktail


class CocktailForm(forms.ModelForm):
    class Meta:
        model = Cocktail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Name',
            'product': 'Product',
            'product_measure': 'Product Quantity',
            'ingredient_1': 'Ingredient 1',
            'ingredient_2': 'Ingredient 2',
            'ingredient_3': 'Ingredient 3',
            'ingredient_4': 'Ingredient 4',
            'ingredient_5': 'Ingredient 5',
            'ingredient_6': 'Ingredient 6',
            'ingredient_7': 'Ingredient 7',
            'method': 'Method',
        }

        for field in self.fields:
            if field != "image":
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].label = False
                self.fields[field].widget.attrs['class'] = 'user-profile-input'
