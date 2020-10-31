from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_a_crate, name='create_a_crate'),
    path('add_to_crate/<product_id>', views.add_to_crate, name='add_to_crate'),
    path('delete_from_crate/<product_id>', views.delete_from_crate,
         name='delete_from_crate'),
    path('empty_crate/', views.empty_crate, name='empty_crate'),
]
