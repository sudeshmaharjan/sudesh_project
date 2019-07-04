from django.shortcuts import render, HttpResponseRedirect
from .models import Employee, Experience, Projects
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy, reverse
from .forms import EmployeeAddForm, AddExperience, ExperienceFormSet, AddProject
from django.views.generic.edit import DeleteView, FormView, UpdateView
from django.db import transaction


class EmployeeList(ListView):
    model = Employee
    template_name = 'employees/list.html'
    context_object_name = 'employees_list'


class EmployeeDetail(DetailView):
    model = Employee
    template_name = 'employees/details.html'
    context_object_name = 'employees_detail'

    def get_context_data(self, **kwargs):
        context = super(EmployeeDetail, self).get_context_data(**kwargs)
        context['experience'] = Experience.objects.filter(employee_id=self.object.id)
        return context


class EmployeeAdd(FormView):
    model = Employee
    template_name = 'employees/new.html'
    success_url = reverse_lazy('employees:employees_list')
    form_class = EmployeeAddForm

    def form_valid(self, form):
        form.save()
        return super(EmployeeAdd, self).form_valid(form)


class EmployeeUpdate(UpdateView):
    model = Employee
    template_name = 'employees/edit.html'
    form_class = EmployeeAddForm

    def get_success_url(self):
        if self.request.method=='POST' and 'btn_exit' in self.request.POST:
            return reverse_lazy('employees:employees_detail', args=(self.object.id,))
        if self.request.method == 'POST' and 'btn_update' in self.request.POST:
            return reverse_lazy('employees:edit', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(EmployeeUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['expform'] = ExperienceFormSet(self.request.POST, instance=self.object)
        else:
            context['expform'] = ExperienceFormSet(instance=self.object)
        context['experience'] = Experience.objects.filter(employee_id=self.object.id)
        return context

    # def form_valid(self, form):
    #     exp = form.save(commit=False)
    #     exp.employee_id = Employee.objects.get(id=self.object.id)
    #     exp.save()
    #     return super(EmployeeUpdate, self).form_valid(form)

    def form_valid(self, form):
        context = self.get_context_data()
        titles = context['expform']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
        return super(EmployeeUpdate, self).form_valid(form)

    
class EmployeeExperience(FormView):
    model = Experience
    template_name = 'employees/experience.html'
    form_class = AddExperience
    

    def get_context_data(self, **kwargs):
        context = super(EmployeeExperience, self).get_context_data(**kwargs)
        context['experience'] = self.get_form()
        return context

    def get_success_url(self):
        return reverse_lazy('employees:employees_detail', args=(self.kwargs['pk'],))

    def form_valid(self, form):
        exp = form.save(commit=False)
        exp.employee_id = Employee.objects.get(id=self.kwargs['pk'])
        exp.save()
        return super(EmployeeExperience, self).form_valid(form)


class EmployeeProjects(FormView):
    model = Projects
    template_name = 'employees/project.html'
    form_class = AddProject

    def get_success_url(self):
        return reverse_lazy('employees:employees_detail', args=(self.kwargs['pk'],))

    def form_valid(self, form):
        pro = form.save(commit=False)
        pro.employee_id = Employee.objects.get(id=self.kwargs['pk'])
        pro.save()
        return super(EmployeeProjects, self).form_valid(form)


class EmployeeDelete(DeleteView):
    model = Employee
    success_url = reverse_lazy('employees:employees_list')
    template_name = 'employees/remove.html'
