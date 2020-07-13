from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
import datetime
from django.db.models import Avg, Sum, Count
from . import models
from . import forms


#Member#
class MemberCreate(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = models.Member
    fields = ('last_name','first_name','id_number', 'pmpsz_number','young', 'dog', 'motor', 'active' )

class MemberUpdate(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    fields = ('id_number', 'pmpsz_number', 'young', 'dog', 'motor', 'active')
    model = models.Member

class MemberList(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = models.Member
    ordering = ['last_name']

class MemberDetail(LoginRequiredMixin,DetailView):
    login_url = '/login/'
    model = models.Member

class MemberDelete(LoginRequiredMixin,DeleteView):
    login_url = '/login/'
    model = models.Member
    success_url = reverse_lazy('time_sheet:member_list')



#Duty#
class DutyCreate(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = models.Duty
    form_class = forms.DutyForm

class DutyUpdate(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    model = models.Duty
    form_class = forms.DutyForm

class DutyList(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = models.Duty
    queryset = models.Duty.objects.order_by('-date')
    paginate_by = 10


class DutyFilterList(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = models.Duty
    paginate_by = 10
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


class DutyDetail(LoginRequiredMixin,DetailView):
    login_url = '/login/'
    model = models.Duty




#Car#
class CarCreate(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = models.Car
    fields = ('owner','car_type', 'car_plate', 'fuel_type', 'ccm', 'color', 'stripped')

class CarUpdate(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    fields = ('owner','car_type', 'fuel_type', 'ccm', 'color', 'stripped')
    model = models.Car

class CarList(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = models.Car

class CarDetail(LoginRequiredMixin,DetailView):
    login_url = '/login/'
    model = models.Car

#####
#querys
#####

@login_required
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

    members = models.Member.objects.all()
    o, r, re, k, e, er, kms, help, retention, caught, missing, signal, other, a, y, d, m, id, tot = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    plates = []
    persons = []
    dates =[]
    id_name=[]
    for duty in duties:
        if str(duty.plate) not in plates and duty.plate != None:
            plates.append(str(duty.plate))
        if str(duty.member) not in persons:
            persons.append(str(duty.member))
        if str(duty.date) not in dates:
            dates.append(str(duty.date))
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
        elif duty.duty_type == 'Er':
            er += duty.hours
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
        tot += duty.hours

    for member in members:
        if member.active:
            a += 1
            if member.id_number:
                id +=1
                id_name.append(member.first_name)
            if member.young:
                y += 1
            if member.dog:
                d += 1
            if member.motor:
                m += 1

    tot_o = o+e
    persons.sort()
    plates.sort()
    dates.sort()
    one_hour = tot/id

    data = {'o':o,'r':r,'re':re,'k':k, 'e':e, 'er':er, 'kms':kms, 'help':help, 'retention':retention, 'caught':caught, 'missing':missing, 'signal':signal, 'other':other, 'tot_o':tot_o,'cars':len(plates),'person':len(persons),'a':a, 'y':y,'d':d,'m':m,'id':id, 'start':start_date, 'end':end_date,'days':len(dates),'plates':plates,'tag':persons,'dates':dates, 'tot':tot, 'one_hour':format(one_hour, '.2f')}

    return render(request,'time_sheet/duty_sum.html',context=data)

@login_required
def member_sum(request):
    if request.GET.get('s') != "":
        start_date = request.GET.get('s')
    else:
        start_date = datetime.date.today().replace(day=1)

    if request.GET.get('e') != "":
        end_date = request.GET.get('e')
    else:
        end_date = datetime.date.today()
    member = request.GET.get('m')
    duties = models.Duty.objects.filter(date__range=[start_date, end_date ], member__exact=member).all()

    o, r, re, k, e, er, kms, help, retention, caught, missing, signal, other, a, y, d, m, id = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    plates = []
    dates =[]

    for duty in duties:
        member = str(duty.member)
        pk=duty.member.pk
        if str(duty.plate) not in plates and duty.plate != None:
            plates.append(str(duty.plate))
        if str(duty.date) not in dates:
            dates.append(str(duty.date))
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
        elif duty.duty_type == 'Er':
            er += duty.hours
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

    tot = o+r+re+k+e+er
    plates.sort()
    dates.sort()
    tot_o = o+e



    data = {'o':o,'r':r,'re':re,'k':k, 'e':e, 'er': er, 'kms':kms, 'help':help, 'retention':retention, 'caught':caught, 'missing':missing, 'signal':signal, 'other':other, 'tot':tot,'cars':len(plates), 'start':start_date, 'end':end_date,'days':len(dates),'plates':plates, 'dates':dates,'tot_o':tot_o,'pk':pk, 'member':member}

    return render(request,'time_sheet/member_sum.html',context=data)

@login_required
def plate_sum(request):
    if request.GET.get('s') != "":
        start_date = request.GET.get('s')
    else:
        start_date = datetime.date.today().replace(day=1)

    if request.GET.get('e') != "":
        end_date = request.GET.get('e')
    else:
        end_date = datetime.date.today()
    plate = request.GET.get('p')
    duties = models.Duty.objects.filter(date__range=[start_date, end_date ], plate__exact=plate).all()

    o, r, re, er, k, e, kms, help, retention, caught, missing, signal, other, a, y, d, m, id = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    members = []
    dates =[]

    for duty in duties:
        if str(duty.member) not in members:
            members.append(str(duty.member))
        pk=duty.plate.pk
        car = (str(duty.plate))
        if str(duty.date) not in dates:
            dates.append(str(duty.date))
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
        elif duty.duty_type == 'Er':
            er += duty.hours
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

    tot = o+r+re+k+e+er
    members.sort()
    dates.sort()
    tot_o = o+e



    data = {'o':o,'r':r,'re':re,'k':k, 'er':er, 'e':e, 'kms':kms, 'help':help, 'retention':retention, 'caught':caught, 'missing':missing, 'signal':signal, 'other':other, 'tot':tot,'members':len(members), 'start':start_date, 'end':end_date,'days':len(dates),'dates':dates,'tot_o':tot_o,'pk':pk, 'car':car, 'users':members}

    return render(request,'time_sheet/car_sum.html',context=data)

def duty_table(request):
    # if request.GET.get('s') != "":
    #     start_date = request.GET.get('s')
    # else:
    #     start_date = datetime.date.today().replace(day=1)
    #
    # if request.GET.get('e') != "":
    #     end_date = request.GET.get('e')
    # else:
    #     end_date = datetime.date.today()
    #     #script: SELECT "time_sheet_duty"."date", "time_sheet_member"."first_name", "time_sheet_member"."last_name", "time_sheet_duty"."duty_type", "time_sheet_duty"."hours" FROM "time_sheet_duty" INNER JOIN "time_sheet_member" ON ("time_sheet_duty"."member_id" = "time_sheet_member"."id") WHERE "time_sheet_member"."active" = 1 GROUP BY "time_sheet_duty"."date","time_sheet_member"."id", "time_sheet_duty"."duty_type" ORDER BY "time_sheet_duty"."date"
    # duties = models.Duty.objects.filter(date__range=[start_date, end_date ]).all()
    # dates =[]
    #
    # for duty in duties:
    #     if str(duty.date) not in dates:
    #         dates.append(str(duty.date))
    #
    # dates.sort()
    #
    # data = {'start':start_date, 'end':end_date}
    # return render(request,'time_sheet/duty_table.html',context=data)
    model = models.Duty
    field_names = list(model._meta.get_fields())
    titles = [f.verbose_name for f in field_names]
    field_Names = [f.name for f in field_names]
    data = [[getattr(ins, name) for name in field_names]
            for ins in model.objects.prefetch_related().all()]
    return render(request, 'duty_table.html', context={'field_names': field_names, 'data': data})
