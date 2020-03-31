from django.contrib import admin
from materials.models import (
    Material,
    MaterialDelivery,
    MaterialCategory,
    MaterialDeliveryPosition,
)


class MaterialDeliveryPositionInline(admin.TabularInline):
    extra = 1
    model = MaterialDeliveryPosition


class MaterialDeliveryAdmin(admin.ModelAdmin):
    inlines = [
        MaterialDeliveryPositionInline,
    ]


admin.site.register(Material)
admin.site.register(MaterialCategory)
admin.site.register(MaterialDelivery, MaterialDeliveryAdmin)
