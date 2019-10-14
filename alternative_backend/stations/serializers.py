from stations.models import Station
from rest_framework import serializers


class StationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Station
        fields = ('id', 'name', 'description')
