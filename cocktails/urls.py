from django.urls import path
from . import views

urlpatterns = [
    path('', views.cocktails, name='cocktails'),
    path('display_cocktail/<int:cocktail_id>', views.display_cocktail,
         name='display_cocktail'),
    path('delete_cocktail/<int:cocktail_id>', views.delete_cocktail,
         name='delete_cocktail'),
]
