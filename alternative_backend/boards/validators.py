from .services import BoardService
from django.conf import settings
from alternative_backend.exceptions import AppException


def validate_code(code):
    if not code:
        raise AppException('code: {} is not valid'.format(code))
    if code < 0:
        raise AppException('code: {} is too small'.format(code))
    if code > 99:
        raise AppException('code {} is too big'.format(code))


def validate_year(year):
    if not year:
        AppException('year: {} is not valid'.format(year))
    if year < 2018:
        raise ValidationError('year: {} is too small'.format(year))
    if year > 2025:
        raise ValidationError('year: {} is too big'.format(year))


def validate_barcode(barcode):
    if len(barcode) < settings.BARCODE_LENGHT:
        raise AppException('barcode: {} is too short'.format(barcode))
    if len(barcode) > settings.BARCODE_LENGHT:
        raise AppException('barcode: {} is too long'.format(barcode))

    if not BoardService().get_company(barcode=barcode):
        raise AppException('not valid company in barcode'.format(barcode))
    if not BoardService().get_model(barcode=barcode):
        raise AppException('not valid board model in barcode'.format(barcode))


    
