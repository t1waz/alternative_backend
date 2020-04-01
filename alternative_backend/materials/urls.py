from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.views import (
    MaterialViewSet,
    MaterialStock,
    MaterialDeliveryViewSet,
    MaterialCategoryViewSet,
)


app_router = DefaultRouter()

app_router.register(r'material_categories', MaterialCategoryViewSet, basename='material_categories')
app_router.register(r'materials', MaterialViewSet, basename='materials')
app_router.register(r'material_supplies', MaterialDeliveryViewSet, basename='material_supplies')

urlpatterns = [
    path(r'material_stock/', MaterialStock.as_view()),
] + app_router.urls
