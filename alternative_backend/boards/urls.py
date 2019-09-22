from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
	BoardCompanyViewSet,
    BoardModelViewSet,
    BoardViewSet,
    BoardScanAPIView,
    ProductionAPIView,
    ProductionDetailAPIView,
    StockAPIView,
    StockDetailAPIView,
)


app_router = DefaultRouter()

app_router.register(r'companies', BoardCompanyViewSet, basename='companies')
app_router.register(r'board_models', BoardModelViewSet, basename='boardmodels')
app_router.register(r'boards', BoardViewSet, basename='boards')

urlpatterns = [
	path(r'add_scan/', BoardScanAPIView.as_view()),
	path(r'production/', ProductionAPIView.as_view()),
	path(r'production/<int:company>', ProductionDetailAPIView.as_view()),
	path(r'stock/', StockAPIView.as_view()),
	path(r'stock/<int:code>', StockDetailAPIView.as_view()),

] + app_router.urls