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
from workers.views import (
    WorkerViewSet,
    NewWorkerScanAPIView
)
from boards.views import (
    BoardScanAPIView,
    ProductionAPIView,
    BarcodeInfoDetailAPIView,
    NewBoardScanAPIView,
    BarcodeInfoAPIView,
    ProductionDetailAPIView,
    StockAPIView,
    StockDetailAPIView
)
from orders.views import (
    OrderViewSet,
    CompanyOrderInfoAPIView,
    CompanyOrderInfoDetailAPIView,
    SendedBoardRecordAPIView
)

router = DefaultRouter()
router.register(r'workers', WorkerViewSet, basename='workers')
router.register(r'orders', OrderViewSet, basename='orders')


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'add_barcode/', NewBoardScanAPIView.as_view()),
    path(r'add_scan/', BoardScanAPIView.as_view()),
    path(r'add_worker_scan/', NewWorkerScanAPIView.as_view()),
    path(r'add_sended_board/', SendedBoardRecordAPIView.as_view()),
    path(r'production/', ProductionAPIView.as_view()),
    path(r'production/<int:company>', ProductionDetailAPIView.as_view()),
    path(r'stock/', StockAPIView.as_view()),
    path(r'stock/<int:code>', StockDetailAPIView.as_view()),
    path(r'order_info/', CompanyOrderInfoAPIView.as_view()),
    path(r'order_info/<int:code>/', CompanyOrderInfoDetailAPIView.as_view()),
    path(r'boards/', BarcodeInfoAPIView.as_view()),
    path(r'boards/<int:barcode>/', BarcodeInfoDetailAPIView.as_view())
] + router.urls
