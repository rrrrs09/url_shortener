from django.urls import path, re_path

from . import views

urlpatterns = [
    path('shorten/', views.shorten_url, name='shorten_url'),
    path('<slug:slug>/', views.redirect_to_url, name='redirect_to_url'),
]
