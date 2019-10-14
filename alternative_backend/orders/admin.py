from django.contrib import admin
from orders.models import (
    Client,
    Order,
    OrderRecord,
    SendedBoard
)


admin.site.register(Client)
admin.site.register(Order)
admin.site.register(OrderRecord)
admin.site.register(SendedBoard)
