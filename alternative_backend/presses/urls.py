from presses.views import PressViewSet
from rest_framework.routers import DefaultRouter


app_router = DefaultRouter()

app_router.register(r'presses',
                    PressViewSet, 
                    basename='presses')

urlpatterns = [] + app_router.urls
