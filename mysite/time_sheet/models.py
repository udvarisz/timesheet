from django.db import models
from django.utils import timezone
from django.urls import reverse, reverse_lazy

# Create your models here.
class Member(models.Model):
    last_name = models.CharField(max_length=256, verbose_name= ('Vezetéknév'))

    first_name = models.CharField(max_length=256, verbose_name= ('Keresztnév'))

    id_number = models.CharField(max_length=20, blank=True, null=True, verbose_name= ('Igazolvány szám'))

    pmpsz_number = models.CharField(max_length=8, unique=True, blank=True, null=True, verbose_name= ('PMPSZ azonosító'))

    young = models.BooleanField(default=False, verbose_name= ('Ifjú polgárőr'))

    dog = models.BooleanField(default=False, verbose_name= ('Kutyás polgárőr'))

    motor = models.BooleanField(default=False, verbose_name= ('Motoros polgárőr'))

    reg_date = models.DateTimeField(default=timezone.now)

    active = models.BooleanField(default=True, verbose_name= ('Aktív tag'))

    class Meta():
        unique_together = ('first_name', 'last_name')
        ordering = ['last_name']

    def __str__(self):
        return self.last_name + ' ' + self.first_name

    def get_absolute_url(self):
        return reverse_lazy('time_sheet:member_list')



class Duty(models.Model):
    s_types = (('O', 'Önálló'),('R','Rendőrrel közös'),('Re','Rendezvénybiztosítás'),('K', 'Kutyás'),('Er','Egyéb rendvédelmi szervvel'), ('E', 'Egyéb'))

    member = models.ForeignKey('time_sheet.Member', on_delete = models.SET_DEFAULT, verbose_name= ('Szolgálatot ellátó személy'), default=5)

    duty_type = models.CharField(max_length=2, choices = s_types, default='O',verbose_name= ('Szolgálat típusa'))

    date = models.DateField(verbose_name= ('Dátum'))

    hours = models.PositiveSmallIntegerField(default=0, verbose_name= ('Szolgálati órák'))

    commander = models.BooleanField(default=False, verbose_name= ('Járőrparancsnok'))

    kms = models.PositiveSmallIntegerField(default=0, verbose_name= ('Megtett kilométerek'))

    plate = models.ForeignKey('time_sheet.Car', on_delete = models.CASCADE, verbose_name= ('Rendszám'), blank=True, null=True)

    help = models.PositiveSmallIntegerField(default=0, verbose_name= ('Segítségnyújtás (fő)'))

    retention = models.BooleanField(default=False, verbose_name= ('Visszatartás'))

    caught = models.BooleanField(default=False, verbose_name= ('Tettenérés'))

    missing = models.BooleanField(default=False, verbose_name= ('Eltűnt személy felkutatása'))

    signal = models.BooleanField(default=False, verbose_name= ('Jelzésadás'))

    other = models.BooleanField(default=False, verbose_name= ('Egyéb eset'))

    class Meta():
        unique_together = ('member', 'date', 'duty_type')


    def __str__(self):
        return str(self.date) + ' - ' + str(self.member) + ' - ' + str(self.duty_type)

    def get_absolute_url(self):
        return reverse_lazy('time_sheet:duty_list')




class Car(models.Model):
    fuel_types = (('B','Benzin'),('D','Gázolaj'),('G','Gáz'))

    car_type = models.CharField(max_length=150, verbose_name= ('Típus'), blank=True, null=True)

    car_plate = models.CharField(max_length=6, verbose_name= ('Rendszám'), unique=True)

    fuel_type = models.CharField(max_length=1, choices = fuel_types, default='O',verbose_name= ('Üzemanyag típusa'))

    ccm = models.PositiveSmallIntegerField(verbose_name= ('Lökettérfogat'))

    owner = models.CharField(max_length=150, verbose_name= ('Tulajdonos'), blank=True, null=True)

    color = models.CharField(max_length=150, verbose_name= ('Szín'), blank=True, null=True)

    stripped = models.BooleanField(default=False, verbose_name= ('Felszerelt járőrautó'))

    def __str__(self):
        return self.car_plate

    def get_absolute_url(self):
        return reverse_lazy('time_sheet:car_list')
