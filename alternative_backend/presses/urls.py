from rest_framework.routers import DefaultRouter
from .views import (
	PressViewSet,
)


app_router = DefaultRouter()

app_router.register(r'presses',
					PressViewSet, 
					basename='presses')

urlpatterns = [

] + app_router.urls
