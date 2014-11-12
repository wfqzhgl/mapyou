from django.contrib import admin

from models import *


class DataLotteryShsqAdmin(admin.ModelAdmin):
    pass


admin.site.register(DataLotteryShsq, DataLotteryShsqAdmin)
