from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from datetime import date
from django.db.models import Avg, Sum, Count
from . import models
from . import forms


#Member#
class MemberCreate(CreateView):
    model = models.Member
    fields = ('last_name','first_name','id_number', 'pmpsz_number','young', 'dog', 'motor', 'active' )

class MemberUpdate(UpdateView):
    fields = ('id_number', 'pmpsz_number', 'young', 'dog', 'motor', 'active')
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
    form_class = forms.DutyForm

class DutyList(ListView):
    model = models.Duty

    ordering = ['date']

class DutyFilterList(ListView):
    model = models.Duty

    ordering = ['date']

    def get_queryset(self):
        if self.request.GET.get('s') != '':
            start_date = self.request.GET.get('s')
        else:
            start_date = '2020-01-01'
        if self.request.GET.get('e') != '':
            end_date = self.request.GET.get('e')
        else:
            end_date = date.today()
        return super().get_queryset().filter(date__range=[start_date, end_date])


class DutyDetail(DetailView):
    model = models.Duty

#Car#
class CarCreate(CreateView):
    model = models.Car
    fields = ('car_type', 'car_plate', 'fuel_type', 'ccm')

class CarUpdate(UpdateView):
    fields = ('car_type', 'fuel_type', 'ccm')
    model = models.Car

class CarList(ListView):
    model = models.Car


#####

def duty_sum(request):
    start_date = request.GET.get('s')
    end_date = request.GET.get('e')
    if start_date != None and end_date != None:
        duties = models.Duty.objects.filter(date__range=[start_date, end_date])
    else:
        duties = models.Duty.objects.all()
    members = models.Member.objects.all()
    o = 0
    r = 0
    re = 0
    k = 0
    e = 0
    kms = 0
    help = 0
    retention = 0
    caught = 0
    missing = 0
    signal = 0
    other = 0
    plates = []
    persons = []
    dates =[]
    for duty in duties:
        plates.append(duty.plate)
        persons.append(duty.member)
        dates.append(duty.date)
        kms += duty.kms
        help += duty.help
        if duty.duty_type == 'O':
            o += duty.hours
        elif duty.duty_type == 'R':
            r += duty.hours
        elif duty.duty_type == 'Re':
            re += duty.hours
        elif duty.duty_type == 'K':
            k += duty.hours
        elif duty.duty_type == 'E':
            e += duty.hours
        if duty.retention:
            retention +=1
        if duty.caught:
            caught +=1
        if duty.missing:
            missing +=1
        if duty.signal:
            signal +=1
        if duty.other:
            other +=1

    tot_o = o+e
    cars=len(set(plates))
    person=len(set(persons))
    days=len(set(dates))

    a = 0
    y = 0
    d = 0
    m = 0
    id = 0
    for member in members:
        if member.id_number:
            id +=1
        if member.active:
            a += 1
        if member.young:
            y += 1
        if member.dog:
            d += 1
        if member.motor:
            m += 1

    data = {'o':o,'r':r,'re':re,'k':k, 'e':e, 'kms':kms, 'help':help, 'retention':retention, 'caught':caught, 'missing':missing, 'signal':signal, 'other':other, 'tot_o':tot_o,'cars':cars,'person':person,'a':a, 'y':y,'d':d,'m':m,'id':id, 'start':start_date, 'end':end_date,'days':days}

    return render(request,'time_sheet/duty_sum.html',context=data)
