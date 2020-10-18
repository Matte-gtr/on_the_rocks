from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('<int:product_id>/', views.product_display, name='product_display'),
    path('site_management/', views.site_management, name='site_management'),
]
