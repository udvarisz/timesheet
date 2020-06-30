from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import datetime
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
    ordering = ['last_name']

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

    ordering = ['-date']

class DutyFilterList(ListView):
    model = models.Duty

    ordering = ['date']

    def get_queryset(self):
        if self.request.GET.get('s') != "":
            start_date = self.request.GET.get('s')
        else:
            start_date = datetime.date.today().replace(day=1)
        if self.request.GET.get('e') != "":
            end_date = self.request.GET.get('e')
        else:
            end_date = datetime.date.today()
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
    if request.GET.get('s') != "":
        start_date = request.GET.get('s')
    else:
        start_date = datetime.date.today().replace(day=1)

    if request.GET.get('e') != "":
        end_date = request.GET.get('e')
    else:
        end_date = datetime.date.today()


    if request.GET.get('t') !="":
        type = request.GET.get('t').title()
        duties = models.Duty.objects.filter(date__range=[start_date, end_date ], duty_type__exact=type).all()
    else:
        duties = models.Duty.objects.filter(date__range=[start_date, end_date ]).all()

    print(start_date)
    print(end_date)
    members = models.Member.objects.all()
    o, r, re, k, e, kms, help, retention, caught, missing, signal, other, a, y, d, m, id = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    plates = []
    persons = []
    dates =[]
    for duty in duties:
        if duty.plate not in plates and duty.plate != None:
            plates.append(duty.plate)
        if duty.member not in persons:
            persons.append(duty.member)
        if duty.date not in dates:
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

    tot_o = o+e

    data = {'o':o,'r':r,'re':re,'k':k, 'e':e, 'kms':kms, 'help':help, 'retention':retention, 'caught':caught, 'missing':missing, 'signal':signal, 'other':other, 'tot_o':tot_o,'cars':len(plates),'person':len(persons),'a':a, 'y':y,'d':d,'m':m,'id':id, 'start':start_date, 'end':end_date,'days':len(dates),'plates':plates,'tag':persons}

    return render(request,'time_sheet/duty_sum.html',context=data)
