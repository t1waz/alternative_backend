from django.contrib import admin
from materials.models import (
    MaterialCategory,
    Material,
)


admin.site.register(MaterialCategory)
admin.site.register(Material)
