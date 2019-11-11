from django.contrib import admin
from boards.models import (
    BoardCompany,
    BoardModel,
    Board,
    BoardScan,
    BoardModelMaterial,
    BoardModelLayout,
)


class BoardModelMaterialInline(admin.TabularInline):
    model = BoardModelMaterial
    extra = 1


class BoardModelAdmin(admin.ModelAdmin):
    inlines = (BoardModelMaterialInline,)


admin.site.register(BoardCompany)
admin.site.register(Board)
admin.site.register(BoardScan)
admin.site.register(BoardModelMaterial)
admin.site.register(BoardModelLayout)
admin.site.register(BoardModel,
                    BoardModelAdmin)
