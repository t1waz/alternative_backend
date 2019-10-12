from django.contrib import admin
from boards.models import (
    BoardCompany,
    BoardModel,
    Board,
    BoardScan
)


admin.site.register(BoardCompany)
admin.site.register(BoardModel)
admin.site.register(Board)
admin.site.register(BoardScan)
