from stations.models import Station
from common.utils import SimpleValidator
from django.core.exceptions import ValidationError


def validate_production_step(**kwargs):
    production_step = kwargs.get('production_step')

    if not production_step:
        return

    if Station.objects.all().count() == 0:
        if production_step != 1:
            raise ValidationError('first station should have production_step value 1')
    else:
        current_last_production_step = Station.objects.all().values_list(
            'production_step', flat=True).order_by('production_step').last()
        if production_step != current_last_production_step + 1:
            raise ValidationError('production_step should raise linear')


class StationValidation(SimpleValidator):
    validators = (validate_production_step,)
