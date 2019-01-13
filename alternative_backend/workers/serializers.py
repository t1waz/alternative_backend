from rest_framework import serializers
from .models import Worker, WorkerScan




class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('name', 'surname', 'username', 'barcode')


class WorkerScanSerializer(serializers.ModelSerializer):
	worker_barcode = serializers.SlugRelatedField(many=False,
												  queryset=Worker.objects.all(),
												  slug_field='barcode')

	def is_valid(self, raise_exception=False):
		return super().is_valid(raise_exception=True)

	class Meta:
		model = WorkerScan
		fields = ('worker_barcode',)