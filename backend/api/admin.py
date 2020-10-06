from django.contrib import admin
from .models import LongUrl, UrlSlug

admin.site.register(LongUrl)
admin.site.register(UrlSlug)
