from django.urls import path

from . import views
from .views import contact_telegram

urlpatterns = [
    path('', views.home, name='home'),
    path('api/contact/', contact_telegram, name='contact-telegram'),

    path('styles/', views.StyleItemView.as_view(), name='styles'),
    path('services/', views.ServicesItemView.as_view(), name='services'),
    path('styles/<int:pk>/', views.StyleItemDetailView.as_view(), name='style_detail'),

    path('materials/', views.materials_list, name='materials_list'),

    path('projects/', views.projects_view, name='projects'),
    path('projects/<int:pk>', views.project_detail, name='project_detail'),

    path('contacts/', views.contacts, name='contacts'),
    path('search/', views.site_search, name='site_search'),
]
