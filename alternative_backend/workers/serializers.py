import datetime
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import (
    Worker,
    WorkerScan
)


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('id', 'name', 'surname', 'username', 'barcode')
        validators = [UniqueTogetherValidator(queryset=Worker.objects.all(),
                                              fields=('username', 'barcode'))]


class WorkerScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerScan
        fields = ('id', 'worker_barcode', 'week', 
                  'day_name', 'year', 'month', 'seconds', 'started')

    worker_barcode = serializers.SlugRelatedField(many=False,
                                                  queryset=Worker.objects.all(),
                                                  slug_field='username')

    def is_valid(self, raise_exception=False):
        now = datetime.datetime.now()
        time_values = {
            'week': int(now.strftime("%V")),
            'day_name': now.strftime("%A"),
            'year': int(now.strftime("%Y")),
            'month': int(now.strftime("%m")),
            'seconds': int(now.strftime("%s")) * 1000}

        self.initial_data.update(time_values)

        return super().is_valid(raise_exception=True)
