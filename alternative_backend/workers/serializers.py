from rest_framework import serializers
from .models import Worker




class WorkerSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Worker
		fields = ('name', 'surname', 'username', 'barcode')