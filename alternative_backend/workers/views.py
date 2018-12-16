from rest_framework import viewsets
from .models import Worker
from .serializers import WorkerSerializer


class WorkerViewSet(viewsets.ModelViewSet):


	serializer_class = WorkerSerializer
	queryset = Worker.objects.all()

