from rest_framework import serializers
from .models import Station




class StationSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Station
		fields = ('id', 'name', 'description')