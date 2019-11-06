from rest_framework import serializers
from workers.services import WorkerService
from rest_framework.validators import UniqueTogetherValidator
from workers.models import (
    Worker,
    WorkerWorkHistory,
)


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('name', 'surname', 'username', 'barcode')
        validators = [UniqueTogetherValidator(queryset=Worker.objects.all(),
                                              fields=('username', 'barcode'))]


class WorkerWorkHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerWorkHistory
        fields = ('worker',)

    def create(self, validated_data):
        return WorkerService().handle_worker_work_history(worker=validated_data.get('worker'))
