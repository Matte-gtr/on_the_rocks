from django.urls import path
from . import views
from .webhooks import webhook


urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('successful_checkout/<order_number>', views.successful_checkout,
         name='successful_checkout'),
    path('cache_checkout_data/', views.cache_checkout_data,
         name='cache_checkout_data'),
    path('webhook', webhook, name='webhook'),
    path('login_prompt/', views.login_prompt, name='login_prompt'),
]
