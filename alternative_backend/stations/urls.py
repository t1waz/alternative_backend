from rest_framework.routers import DefaultRouter
from .views import (
	StationViewSet,
)


app_router = DefaultRouter()

app_router.register(r'stations', StationViewSet, basename='stations')

urlpatterns = [

] + app_router.urls