from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from . import models
from . import forms


class MemberCreate(CreateView):
    model = models.Member
    fields = ('last_name','first_name','id_number', 'pmpsz_number')



class MemberUpdate(UpdateView):
    fields = ('id_number', 'pmpsz_number')
    model = models.Member

    redirect_field_name = '/thanks.html'

class DutyCreate(CreateView):
    model = models.Duty
    form_class = forms.DutyForm



class DutyUpdate(UpdateView):
    model = models.Duty
    form_class = forms.DutyUpdateForm

    
