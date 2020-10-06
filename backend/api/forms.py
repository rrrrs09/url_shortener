from django import forms
from django.core.exceptions import ValidationError

from .models import UrlSlug


class UrlForm(forms.Form):
    url = forms.URLField()
    slug = forms.SlugField(required=False, max_length=50)

    def __init__(self, *args, **kwargs):
        self.host_url = kwargs.pop('host_url', None)
        super(UrlForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get('url')
        slug = cleaned_data.get('slug')

        if slug and UrlSlug.objects.filter(slug=slug).exists():
            error = ValidationError(
                'This slug is already in use.',
                'already_exists'
            )
            self.add_error('slug', error)

        if url and self.host_url is not None:
            if url.startswith(self.host_url):
                error = ValidationError(
                    'This link is already shortened.',
                    'service_url'
                )
                self.add_error('url', error)