from rest_framework import serializers

from stations.models import Station
from stations.validators import StationValidation


class StationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Station
        fields = ('id', 'name', 'description', 'production_step')
        validators = [StationValidation()]
