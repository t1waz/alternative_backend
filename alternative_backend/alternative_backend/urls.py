"""alternative_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from workers.views import WorkerViewSet
from boards.views import BoardScanAPIView, ProductionAPIView
from orders.views import OrderViewSet

router = DefaultRouter()
router.register(r'workers', WorkerViewSet, basename='workers')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'scans/', BoardScanAPIView.as_view()),
    path(r'production/', ProductionAPIView.as_view()),
] + router.urls
