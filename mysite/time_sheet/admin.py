from django.contrib import admin
from . import models
# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    list_display=['last_name','first_name','pmpsz_number']

class DutyAdmin(admin.ModelAdmin):
    list_display=['date', 'member', 'duty_type', 'plate']

class CarAdmin(admin.ModelAdmin):
    list_display=['car_plate', 'car_type', 'owner']

admin.site.register(models.Member,MemberAdmin)
admin.site.register(models.Duty,DutyAdmin)
admin.site.register(models.Car,CarAdmin)
