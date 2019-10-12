from rest_framework.routers import DefaultRouter
from materials.views import (
    MaterialCategoryViewSet,
    MaterialViewSet,
)


app_router = DefaultRouter()

app_router.register(r'material_categories', 
                    MaterialCategoryViewSet, 
                    basename='material_categories')
app_router.register(r'materials',
                    MaterialViewSet,
                    basename='materials')

urlpatterns = [] + app_router.urls
