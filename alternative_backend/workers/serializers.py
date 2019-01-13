from rest_framework import serializers
from .models import Worker, WorkerScan
import datetime



class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('name', 'surname', 'username', 'barcode')


class WorkerScanSerializer(serializers.ModelSerializer):
	worker_barcode = serializers.SlugRelatedField(many=False,
												  queryset=Worker.objects.all(),
												  slug_field='barcode')

	def is_valid(self, raise_exception=False):
		now = datetime.datetime.now()		
		missing_values = {	'week': int(now.strftime("%V")),
							'day_name': now.strftime("%A"),
							'year': int(now.strftime("%Y")),
							'month': int(now.strftime("%m")),
							'seconds': int(now.strftime("%s")) * 1000
						}

		self.initial_data.update(missing_values)

		return super().is_valid(raise_exception=True)

	class Meta:
		model = WorkerScan
		fields = ('worker_barcode','week', 'day_name', 'year', 'month', 'seconds')