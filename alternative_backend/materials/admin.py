from django.contrib import admin
from materials.models import (
    MaterialCategory,
    Material,
    BoardModelComponent,
)


admin.site.register(MaterialCategory)
admin.site.register(Material)
admin.site.register(BoardModelComponent)
