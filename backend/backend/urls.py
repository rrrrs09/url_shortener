from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import TemplateView


urlpatterns = [
    path('', include('api.urls')),
    path('', TemplateView.as_view(template_name='index.html')),
]
if settings.DEBUG:
    urlpatterns = [path('admin/', admin.site.urls)] + urlpatterns
