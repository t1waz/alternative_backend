from rest_framework.routers import DefaultRouter
from .views import (
	ClientViewSet,
	OrderViewSet,
	CompanyOrderInfoAPIView,
    CompanyOrderInfoDetailAPIView,
    SendedBoardRecordAPIView,
)


app_router = DefaultRouter()

app_router.register(r'clients', ClientViewSet, basename='clients')
app_router.register(r'orders', OrderViewSet, basename='orders')


urlpatterns = [
    path(r'add_sended_board/', SendedBoardRecordAPIView.as_view()),
    path(r'order_info/', CompanyOrderInfoAPIView.as_view()),
    path(r'order_info/<int:code>/', CompanyOrderInfoDetailAPIView.as_view()),
] + app_router.urls
