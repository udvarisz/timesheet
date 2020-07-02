from django import forms
from time_sheet.models import Duty

class DutyForm(forms.ModelForm):

    class Meta:
        model = Duty
        fields = ('date', 'member','duty_type', 'hours', 'commander', 'kms', 'plate', 'help', 'retention', 'caught', 'missing', 'signal','other')
        widgets = {
        'date':forms.DateInput(attrs={'class':'datepicker'}),
        'duty_type':forms.RadioSelect(),
        'plate':forms.RadioSelect(),
        'commander':forms.CheckboxInput(attrs={'class':'duty commander'}),
        }

class DutyUpdateForm(forms.ModelForm):

    class Meta:
        fields = ('member','duty_type', 'date', 'hours', 'commander', 'kms', 'plate', 'retention', 'caught', 'missing', 'signal', 'other')
        widgets = {
        'date':forms.DateInput(attrs={'class':'datepicker'}),
        'duty_type':forms.RadioSelect(),
        'plate':forms.RadioSelect(),
        'commander':forms.CheckboxInput(attrs={'class':'duty commander'}),
        }

class DutyMemberForm(forms.ModelForm):
    class Meta():
        model = Duty
        fields =('member',) 
