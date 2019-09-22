from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
	WorkerViewSet,
	NewWorkerScanAPIView,
)


app_router = DefaultRouter()

app_router.register(r'workers', WorkerViewSet, basename='workers')

urlpatterns = [
	path(r'add_worker_scan/', NewWorkerScanAPIView.as_view()),
] + app_router.urls
