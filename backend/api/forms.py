from django import forms


class UrlForm(forms.Form):
    long_url = forms.URLField()
    slug = forms.SlugField(required=False, max_length=50)