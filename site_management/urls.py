from django.urls import path
from . import views

urlpatterns = [
    path('', views.site_management, name='site_management'),
    path('approve_review/<int:review_id>/', views.approve_review,
         name='approve_review'),
    path('delete_review/<int:review_id>/', views.delete_review,
         name='delete_review'),
    path('user_profile/<user_id>/', views.user_profile,
         name='user_profile'),
    path('order_history/<order_id>/', views.order_history,
         name='order_history'),
]
