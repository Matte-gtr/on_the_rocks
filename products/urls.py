from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('<int:product_id>/', views.product_display, name='product_display'),
    path('add_product/', views.add_product, name='add_product'),
]
