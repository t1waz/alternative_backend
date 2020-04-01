from django.contrib import admin

from orders.models import (
    Order,
    Client,
    OrderRecord,
    SendedBoard,
)


class OrderRecordInline(admin.TabularInline):
    model = OrderRecord
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderRecordInline,)
    exclude = ('boards',)


admin.site.register(Client)
admin.site.register(SendedBoard)
admin.site.register(OrderRecord)
admin.site.register(Order,
                    OrderAdmin)
