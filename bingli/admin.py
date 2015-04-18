from django.contrib import admin

# Register your models here.
from models import *

class PatientAdmin(admin.ModelAdmin):
    pass

class BTypeAdmin(admin.ModelAdmin):
    pass

class BHistoryAdmin(admin.ModelAdmin):
    pass

class BCategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(BCategory, BCategoryAdmin)

admin.site.register(Patient, PatientAdmin)
admin.site.register(BType, BTypeAdmin)
admin.site.register(BHistory, BHistoryAdmin)
