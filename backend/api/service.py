import json

from hashids import Hashids
from django.core.validators import URLValidator, validate_slug
from django.core.exceptions import ValidationError

from .models import *


hashids = Hashids(min_length=6)

class ApiValidator:
    '''Static class for validating user url and slug'''
    @staticmethod
    def validate_url(url):
        if not url:
            error = ValidationError(
                code='url_is_required',
                message='Url field could not be blank.'
            )
            error.status = 422
            raise error

        validator = URLValidator()
        try:
            validator(url)
        except ValidationError as error:
            error.code = 'invalid_url'
            error.message = 'Pass the correct url.'
            error.status = 422
            raise error

        return url

    @staticmethod
    def validate_url_slug(slug):
        if not slug:
            return None

        error_code = 'invalid_slug'
        error_message = ('Slug must contain only numbers, letters, '
                'underscores or hyphens and be no more than 50 characters.')
        slug = slug.strip(' -_')
        if len(slug) >= 50:
            error = ValidationError(code=error_code, message=error_message)
            error.status = 422
            raise error
        try:
            validate_slug(slug)
        except ValidationError as error:
            error.code = error_code
            error.message = error_message
            error.status = 422
            raise error

        try:
            UrlSlug.objects.get(slug=slug)
        except UrlSlug.DoesNotExist:
            pass
        else:
            error = ValidationError(
                code='slug_already_exists',
                message='This slug is already in use.'
            )
            error.status = 422
            raise error

        return slug


def post(request):
    '''
    If the data is valid inserts the data and returns a token or slug
    '''
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        error = ValidationError(
            code='invalid_data',
            message='data processing problems',
        )
        error.status = 400
        raise error

    try:
        validated_url = ApiValidator.validate_url(data.get('url'))
        validated_slug = ApiValidator.validate_url_slug(data.get('slug'))
    except ValidationError as error:
        raise error

    long_url, _ = LongUrl.objects.get_or_create(url=validated_url)
    if validated_slug is not None:
        UrlSlug.objects.create(
            long_url=long_url,
            slug=validated_slug
        )
        return validated_slug

    return hashids.encode(long_url.id)
