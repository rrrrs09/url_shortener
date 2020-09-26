from django.urls import path, re_path

from . import views


urlpatterns = [
    path('shorten/', views.shorten_url),
    re_path(r'^(?P<path>([A-Za-z\d]+-{1})*[A-Za-z\d]{1,})/$',
            views.redirect_to_url),
]
