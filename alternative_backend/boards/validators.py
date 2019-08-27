from django.core.exceptions import ValidationError


def validate_code(value):
    if value < 0:
        raise ValidationError('code: {} is too small'.format(value))
    elif value > 99:
        raise ValidationError('code {} is too big'.format(value))


def validate_year(value):
    if value < 2018:
        raise ValidationError('year: {} is too small'.format(value))
    elif value > 2025:
        raise ValidationError('year: {} is too big'.format(value))
