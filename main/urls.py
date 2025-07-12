from django.urls import path

from . import views
from .views import contact_telegram

urlpatterns = [
    path('', views.home, name='home'),
    path('api/contact/', contact_telegram, name='contact-telegram'),

    path('styles/', views.styles, name='styles'),
    path('products/', views.products, name='products'),
    path('projects/', views.projects, name='projects'),
    path('contacts/', views.contacts, name='contacts'),
]
