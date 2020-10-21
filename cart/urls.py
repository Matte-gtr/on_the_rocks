from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add_to_cart/<product_id>', views.add_to_cart,
         name='add_to_cart'),
    path('update_quantity/<product_id>', views.update_quantity,
         name='update_quantity'),
    path('delete_from_cart/<product_id>', views.delete_from_cart,
         name='delete_from_cart'),
]
