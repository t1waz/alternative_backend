from django.conf import settings
from .services import BoardService
from common.common import SimpleValidator
from django.core.exceptions import ValidationError


def validate_code(**kwargs):
    code = kwargs.get('code')
    if code < 0:
        raise ValidationError('code: {} is too small'.format(code))
    if code > 99:
        raise ValidationError('code {} is too big'.format(code))


def validate_year(**kwargs):
    year = kwargs.get('year')
    if year < 2018:
        raise ValidationError('year: {} is too small'.format(year))
    if year > 2025:
        raise ValidationError('year: {} is too big'.format(year))


def validate_barcode(**kwargs):
    barcode = kwargs.get('barcode')
    if len(str(barcode)) < settings.BARCODE_LENGHT:
        raise ValidationError('barcode: {} is too short'.format(barcode))
    if len(str(barcode)) > settings.BARCODE_LENGHT:
        raise ValidationError('barcode: {} is too long'.format(barcode))

    if not BoardService().get_company(barcode=barcode):
        raise ValidationError('not valid company in barcode'.format(barcode))
    if not BoardService().get_model_from_barcode(barcode=barcode):
        raise ValidationError('not valid board model in barcode'.format(barcode))


class BoardCompanyValidation(SimpleValidator):
    validators = (validate_code,)


class BoardModelValidation(SimpleValidator):
    validators = (validate_year,)


class BoardValidation(SimpleValidator):
    validators = (validate_barcode,)
