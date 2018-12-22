from rest_framework import viewsets
from .models import BoardScan
from .serializers import BoardScanSerializer
from common.auth import BaseAccess


class BoardScanViewSet(viewsets.ModelViewSet):

	serializer_class = BoardScanSerializer
	queryset = BoardScan.objects.all()
#	permission_classes = [BaseAccess]