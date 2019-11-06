from django.urls import path
from rest_framework.routers import DefaultRouter
from workers.views import (
	WorkerViewSet,
	WorkerWorkHistoryAPIView,
	WorkerLoginAPIView,
	WorkerTokenValidate,
)


app_router = DefaultRouter()

app_router.register(r'workers', WorkerViewSet, basename='workers')

urlpatterns = [
	path(r'worker_scan/', WorkerWorkHistoryAPIView.as_view()),
	path(r'login/', WorkerLoginAPIView.as_view()),
	path(r'validate_token/', WorkerTokenValidate.as_view()),
] + app_router.urls
