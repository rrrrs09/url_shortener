from hashids import Hashids
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.core.exceptions import ValidationError
from django.http import (JsonResponse, HttpResponseRedirect,
                         HttpResponseNotFound)

from .models import LongUrl, UrlSlug
from .service import post


hashids = Hashids(min_length=6)

@csrf_exempt
@require_POST
def shorten_url(request):
    try:
        shortened_url = post(request)
    except ValidationError as error:
        data = {
            'error': {
                'code': error.code,
                'message': error.message
            }
        }
        return JsonResponse(data, status=error.status)

    return JsonResponse({
        'url': request.build_absolute_uri(f'/{shortened_url}/')
    }, status=201)


@require_GET
def redirect_to_url(request, slug):
    decoded_slug = hashids.decode(slug)
    if decoded_slug:
        url_id = decoded_slug[0]
        try:
            url = LongUrl.objects.get(id=url_id).url
        except LongUrl.DoesNotExist:
            return HttpResponseNotFound()
    else:
        try:
            url_slug = UrlSlug.objects.get(slug=slug)
            url = url_slug.long_url.url
        except UrlSlug.DoesNotExist:
            return HttpResponseNotFound()

    return HttpResponseRedirect(url)
