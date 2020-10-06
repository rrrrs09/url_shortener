import json

from hashids import Hashids

from .models import LongUrl, UrlSlug
from .forms import UrlForm

hashids = Hashids(min_length=6)


def post_data(request):
    try:
        request_data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        response_data = {
            'error': {
                'message': 'json processing problems',
                'code': 'invalid_json'
            }
        }
        return response_data, 400

    data = {
        'url': request_data.get('url'),
        'slug': request_data.get('slug')
    }
    host_url = request.build_absolute_uri('/')[:-1]
    form = UrlForm(data, host_url=host_url)

    if form.is_valid():
        token = None
        validated_url = form.cleaned_data['url']
        validated_slug = form.cleaned_data['slug']

        url, _ = LongUrl.objects.get_or_create(url=validated_url)
        if validated_slug:
            UrlSlug.objects.create(long_url=url, slug=validated_slug)
            token = validated_slug

        if token is None:
            token = hashids.encode(url.id)

        response_data = {
            'url': request.build_absolute_uri(f'/{token}/')
        }
        return response_data, 201
    else:
        response_data = {
            'errors': form.errors.get_json_data()
        }
        return response_data, 422
