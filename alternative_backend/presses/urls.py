from django.urls import path
from rest_framework.routers import DefaultRouter
from presses.views import (
    PressViewSet,
    MoldChangeApiView
)


app_router = DefaultRouter()

app_router.register(r'presses',
                    PressViewSet, 
                    basename='presses')

urlpatterns = [
    path(r'change_mold/', MoldChangeApiView.as_view()),
] + app_router.urls
