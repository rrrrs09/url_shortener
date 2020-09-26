import json

from hashids import Hashids
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import (JsonResponse, HttpResponseRedirect,
                         HttpResponseNotFound)

from .models import UrlItem, UrlSlug
from .service import *


hashids = Hashids(min_length=6)

@csrf_exempt
@require_POST
def shorten_url(request):
    body = request.body.decode('utf-8')
    data = json.loads(body)
    original_url = data.get('url')

    if original_url is None or not original_url:
        return JsonResponse(get_response(False, code='urlIsRequired'),
                            status=422)
    if not is_url(original_url):
        return JsonResponse(get_response(False, code='invalidUrl'),
                            status=422)

    url_slug = None
    slug = data.get('slug')
    if slug is not None and slug:
        validated_slug = validate_slug(slug)
        if validated_slug is None:
            return JsonResponse(
                get_response(False, code='slugValidation'), status=422)

        if UrlSlug.objects.filter(slug=validated_slug).exists():
            return JsonResponse(
                get_response(False, code='slugAlreadyExists'),
                status=422
            )

        url_slug = UrlSlug(slug=validated_slug)

    url_item, _ = UrlItem.objects.get_or_create(original_url=original_url)
    if url_slug is not None:
        url_slug.url = url_item
        url_slug.save()

    # token if slug is None
    shortened_url = url_slug or hashids.encode(url_item.id)
    response = get_response(True, data={
        'url': request.build_absolute_uri(f'/{shortened_url}/')})

    return JsonResponse(response ,status=201)


def redirect_to_url(request, path):
    result = hashids.decode(path)
    if result:
        url_id = result[0]
        try:
            url = UrlItem.objects.get(id=url_id).original_url
        except UrlItem.DoesNotExist:
            return HttpResponseNotFound()
    else:
        try:
            url_slug = UrlSlug.objects.get(slug=path)
            url = url_slug.url.original_url
        except UrlSlug.DoesNotExist:
            return HttpResponseNotFound()

    return HttpResponseRedirect(url)
