from django.contrib import admin

from boards.models import (
    Board,
    Layout,
    BoardScan,
    BoardModel,
    BoardCompany,
    BoardModelMaterial,
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
admin.site.register(Layout)
admin.site.register(BoardModel, BoardModelAdmin)
