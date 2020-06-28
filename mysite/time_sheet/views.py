from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from . import models
from . import forms

#Member#
class MemberCreate(CreateView):
    model = models.Member
    fields = ('last_name','first_name','id_number', 'pmpsz_number')

class MemberUpdate(UpdateView):
    fields = ('id_number', 'pmpsz_number')
    model = models.Member

class MemberList(ListView):
    model = models.Member

class MemberDetail(DetailView):
    model = models.Member

class MemberDelete(DeleteView):
    model = models.Member
    success_url = reverse_lazy('time_sheet:member_list')



#Duty#
class DutyCreate(CreateView):
    model = models.Duty
    form_class = forms.DutyForm


class DutyUpdate(UpdateView):
    model = models.Duty
    form_class = forms.DutyUpdateForm

#Car#
class CarCreate(CreateView):
    model = models.Car
    fields = ('car_type', 'car_plate', 'fuel_type', 'ccm')

class CarUpdate(UpdateView):
    fields = ('car_type', 'fuel_type', 'ccm')
    model = models.Car

class CarList(ListView):
    model = models.Car

    # def get_queryset(self):
    #     pass
