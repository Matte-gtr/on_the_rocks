from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_a_crate, name='create_a_crate'),
]
