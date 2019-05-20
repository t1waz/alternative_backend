from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from stations.views import StationViewSet
from presses.views import PressViewSet
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
    StockDetailAPIView,
    BoardSecondCategoryAPIView,
    BoardCompanyViewSet
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
router.register(r'stations', StationViewSet, basename='stations')
router.register(r'presses', PressViewSet, basename='presses')
router.register(r'companies', BoardCompanyViewSet, basename='companies')


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'add_barcode/', NewBoardScanAPIView.as_view()),
    path(r'add_scan/', BoardScanAPIView.as_view()),
    path(r'add_worker_scan/', NewWorkerScanAPIView.as_view()),
    path(r'add_sended_board/', SendedBoardRecordAPIView.as_view()),
    path(r'add_second_category/', BoardSecondCategoryAPIView.as_view()),
    path(r'production/', ProductionAPIView.as_view()),
    path(r'production/<int:company>', ProductionDetailAPIView.as_view()),
    path(r'stock/', StockAPIView.as_view()),
    path(r'stock/<int:code>', StockDetailAPIView.as_view()),
    path(r'order_info/', CompanyOrderInfoAPIView.as_view()),
    path(r'order_info/<int:code>/', CompanyOrderInfoDetailAPIView.as_view()),
    path(r'boards/', BarcodeInfoAPIView.as_view()),
    path(r'boards/<int:barcode>/', BarcodeInfoDetailAPIView.as_view()),
] + router.urls
