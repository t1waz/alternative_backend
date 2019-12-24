from django.contrib import admin
from materials.models import (
    Material,
    MaterialDelivery,
    MaterialCategory,
    MaterialDeliveryPosition,
)


admin.site.register(Material)
admin.site.register(MaterialCategory)
admin.site.register(MaterialDelivery)
admin.site.register(MaterialDeliveryPosition)