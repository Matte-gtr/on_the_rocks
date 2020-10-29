from django.urls import path
from . import views

urlpatterns = [
    path('', views.cocktails, name='cocktails'),
    path('display_cocktail/<int:cocktail_id>', views.display_cocktail,
         name='display_cocktail'),
    path('delete_cocktail/<int:cocktail_id>', views.delete_cocktail,
         name='delete_cocktail'),
    path('add_cocktail/', views.add_cocktail,
         name='add_cocktail'),
    path('edit_cocktail/<int:cocktail_id>', views.edit_cocktail,
         name='edit_cocktail'),
]
