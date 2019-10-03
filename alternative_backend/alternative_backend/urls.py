from django.urls import path
from django.contrib import admin
from boards.urls import urlpatterns as boards_urlpatterns
from orders.urls import urlpatterns as orders_urlpatterns
from presses.urls import urlpatterns as presses_urlpatterns
from stations.urls import urlpatterns as stations_urlpatterns
from workers.urls import urlpatterns as workers_urlpatterns


app_urlpatterns = boards_urlpatterns + \
                  orders_urlpatterns + \
                  presses_urlpatterns + \
                  stations_urlpatterns + \
                  workers_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
] + app_urlpatterns
