from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from common.auth import BaseAccess


class OrderViewSet(viewsets.ModelViewSet):
	
	serializer_class = OrderSerializer
	queryset = Order.objects.all()
	permission_classes = [BaseAccess]
