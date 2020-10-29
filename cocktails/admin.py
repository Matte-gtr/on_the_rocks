from django.contrib import admin
from .models import Cocktail


class CocktailAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'product',
        'product_measure',
        'ingredient_1',
        'ingredient_2',
        'ingredient_3',
        'ingredient_4',
        'ingredient_5',
        'ingredient_6',
        'ingredient_7',
        'method',
        'image'
    ]


admin.site.register(Cocktail, CocktailAdmin)
