from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'time_sheet'

urlpatterns = [
    path('new_member/',views.MemberCreate.as_view(),name='member_create'),
    path('update_member/<int:pk>/',views.MemberUpdate.as_view(), name='member_update'),
    path('member_detail/<int:pk>/', views.MemberDetail.as_view(), name='member_detail'),
    path('member_list/',views.MemberList.as_view(), name='member_list'),
    path('all_member/',views.all_member, name='all_member'),
    path('member_delete/<int:pk>/', views.MemberDelete.as_view(), name='member_delete'),
    path('member_sum/',views.member_sum, name='member_sum'),
    path('new_duty/',views.DutyCreate.as_view(), name='duty_create'),
    path('update_duty/<int:pk>/',views.DutyUpdate.as_view(), name='duty_update'),
    path('duty_list/', views.DutyList.as_view(), name='duty_list'),
    path('duty_detail/<int:pk>/', views.DutyDetail.as_view(), name='duty_detail'),
    path('duty_list_filter/', views.DutyFilterList.as_view(), name='duty_filter_list'),
    path('duty_sum/',views.duty_sum, name='duty_sum'),
    path('duty_table/',views.duty_table, name='duty_table'),
    path('duty_member_sum/',views.duty_member_sum, name='duty_member_sum'),
    path('new_car/',views.CarCreate.as_view(), name='car_create'),
    path('udpate_car/<int:pk>', views.CarUpdate.as_view(), name='car_update'),
    path('list_car/',views.CarList.as_view(), name='car_list'),
    path('car_detail/<int:pk>/', views.CarDetail.as_view(), name='car_detail'),
    path('car_sum/',views.plate_sum, name='car_sum'),

    ]
