from django.forms import ModelForm
from .models import Employee, Experience, Projects, Task, Invite
from django.forms.models import inlineformset_factory
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput
from django import forms
import datetime

class InviteForm(ModelForm):
    model = Invite
    fields = '__all__'

class EmployeeAddForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'


class AddExperience(ModelForm):
    class Meta:
        model = Experience

        field = forms.CharField(
            label='Field',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Field'
            })
        )
        years = forms.IntegerField(
            label='Years',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Years'
            })
        )
        # fields = '__all__'
        exclude = ('employee_id',)



ExperienceFormSet = inlineformset_factory(Employee, Experience, form=AddExperience, extra=1)

class AddProject(ModelForm):
    class Meta:
        model = Projects
        # fields = '__all__'
        exclude = ('project_begin',)
        widgets = {
            'project_begin': DatePickerInput(format='%Y-%m-%d'), # specify date-frmat
        }


class AddTask(ModelForm):
    class Meta:
        model = Task
        exclude = ('project',)
        widgets = {
            'start_dt': DateTimePickerInput(),
            'end_dt': DateTimePickerInput(),
        }
        