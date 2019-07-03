from django.forms import ModelForm
from .models import Employee, Experience
from django.forms.models import inlineformset_factory


class EmployeeAddForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'


class AddExperience(ModelForm):
    class Meta:
        model = Experience
        # fields = '__all__'
        exclude = ('employee_id',)

ExperienceFormSet = inlineformset_factory(Employee, Experience, form=AddExperience, extra=1)

# class AddProject(ModelForm):
#     class Meta:
#         model = Projects
#         # fields = '__all__'
#         exclude = ('employee_id',)