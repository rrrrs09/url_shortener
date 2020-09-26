import re

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


ERRORS = {
    'urlIsRequired': 'Url could not be blank.',
    'invalidUrl': 'Url is not valid.',
    'slugValidation': 'Slug must contain only numbers, letters and dashes.',
    'slugAlreadyExists': 'Slug is already in use.',
}

def get_response(success, data=None, code=None):
    if success:
        return {
            'success': success,
            'data': data
        }
    else:
        return {
            'success': success,
            'error': {
                'code': code,
                'message': ERRORS.get(code)
            }
        }


def validate_slug(slug):
    SLUG_PATTERN = r'^([A-Za-z\d]+-{1})*[A-Za-z\d]{1,}$'
    slug = slug.strip(' -')
    if re.fullmatch(SLUG_PATTERN, slug) is None:
        return None
    return slug


def is_url(url):
    validator = URLValidator()
    try:
        validator(url)
    except ValidationError:
        return False
    return True
