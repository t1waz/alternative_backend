from django.conf import settings
from boards.services import BoardService
from common.utils import SimpleValidator
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

    if not BoardService().get_company_from_barcode(barcode=barcode):
        raise ValidationError('not valid company in barcode'.format(barcode))
    if not BoardService().get_model_from_barcode(barcode=barcode):
        raise ValidationError('not valid board model in barcode'.format(barcode))


def validate_board_model_component_data(**kwargs):
    if any((True for key in ('material', 'quantity') if key not in kwargs.keys())):
        raise ValidationError('incorrect data for update')


class BoardCompanyValidation(SimpleValidator):
    validators = (validate_code,)


class BoardModelValidation(SimpleValidator):
    validators = (validate_year,
                  validate_code,)


class BoardValidation(SimpleValidator):
    validators = (validate_barcode,)


class BoardModelMaterialValidation(SimpleValidator):
    validators = (validate_board_model_component_data,)
