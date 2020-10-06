from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.http import (JsonResponse, HttpResponseRedirect,
                         HttpResponseNotFound)

from .models import LongUrl, UrlSlug
from .service import post_data, hashids


@csrf_exempt
@require_POST
def shorten_url(request):
    data, status = post_data(request)

    return JsonResponse(data, status=status)


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
