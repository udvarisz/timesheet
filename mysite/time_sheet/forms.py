from django import forms
from time_sheet.models import Duty

class DutyForm(forms.ModelForm):

    class Meta:
        model = Duty
        fields = ('member','duty_type', 'date', 'hours', 'commander', 'kms', 'plate', 'retention', 'caught', 'missing', 'signal', 'other')
        widgets = {
        'date':forms.DateInput(attrs={'class':'datepicker'}),
        'commander':forms.CheckboxInput(attrs={'class':'duty commander'}),
        'kms': forms.NumberInput(attrs={'class': 'duty hidden'}),
        'plate': forms.TextInput(attrs={'class': 'duty hidden'}),
        'help': forms.NumberInput(attrs={'class': 'duty hidden'}),
        'retention':forms.CheckboxInput(attrs={'class':'duty hidden'}),
        'caught':forms.CheckboxInput(attrs={'class':'duty hidden'}),
        'missing':forms.CheckboxInput(attrs={'class':'duty hidden'}),
        'signal':forms.CheckboxInput(attrs={'class':'duty hidden'}),
        'other':forms.CheckboxInput(attrs={'class':'duty hidden'}),
        }
        
class DutyUpdateForm(forms.ModelForm):

    class Meta:
        fields = ('member','duty_type', 'date', 'hours', 'commander', 'kms', 'plate', 'retention', 'caught', 'missing', 'signal', 'other')
