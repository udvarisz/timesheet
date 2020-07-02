from django.contrib import admin
from . import models
# Register your models here.


class DutyAdmin(admin.ModelAdmin):
    list_display=['date', 'member', 'duty_type', 'plate']


admin.site.register(models.Member)
admin.site.register(models.Duty,DutyAdmin)
admin.site.register(models.Car)
