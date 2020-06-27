from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'time_sheet'

urlpatterns = [
    path('new_member/',views.MemberCreate.as_view(),name='member_create'),
    path('update_member/<int:pk>',views.MemberUpdate.as_view(), name='member_update'),
    path('new_duty/',views.DutyCreate.as_view(), name='duty_create'),
    path('update_duty/',views.DutyUpdate.as_view(), name='duty_update')
    ]
