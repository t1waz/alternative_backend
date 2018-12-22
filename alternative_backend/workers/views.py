from rest_framework import viewsets
from .models import Worker
from .serializers import WorkerSerializer
from common.auth import BaseAccess


class WorkerViewSet(viewsets.ModelViewSet):
	
	serializer_class = WorkerSerializer
	queryset = Worker.objects.all()
	permission_classes = [BaseAccess]

