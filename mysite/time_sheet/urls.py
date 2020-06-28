from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'time_sheet'

urlpatterns = [
    path('new_member/',views.MemberCreate.as_view(),name='member_create'),
    path('update_member/<int:pk>',views.MemberUpdate.as_view(), name='member_update'),
    path('new_duty/',views.DutyCreate.as_view(), name='duty_create'),
    path('update_duty/<int:pk>',views.DutyUpdate.as_view(), name='duty_update'),
    path('new_car/',views.CarCreate.as_view(), name='car_create'),
    path('udpate_car/<int:pk>', views.CarUpdate.as_view(), name='car_update'),
    ]
