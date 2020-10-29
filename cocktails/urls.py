from django.urls import path
from . import views

urlpatterns = [
    path('', views.cocktails, name='cocktails'),
    path('display_cocktail/<cocktail_id>', views.display_cocktail,
         name='display_cocktail'),
]
