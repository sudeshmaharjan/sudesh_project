from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .models import Employee, Experience, Projects, Task
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy, reverse
from .forms import EmployeeAddForm, AddExperience, ExperienceFormSet, AddProject, AddTask
from django.views.generic.edit import DeleteView, FormView, UpdateView
from django.db import transaction
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin


class EmployeeList(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employees/list.html'
    context_object_name = 'employees_list'


class EmployeeDetail(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'employees/details.html'
    context_object_name = 'employees_detail'

    def get_context_data(self, **kwargs):
        context = super(EmployeeDetail, self).get_context_data(**kwargs)
        context['experience'] = Experience.objects.filter(employee_id=self.object.id)
        # context['projects'] = Projects.objects.filter(employee_id=self.object.id)
        context['task'] = Task.objects.filter(employee_id=self.object.id)
        return context


class EmployeeAdd(LoginRequiredMixin, FormView):
    model = Employee
    template_name = 'employees/new.html'
    success_url = reverse_lazy('employees:dashboard')
    form_class = EmployeeAddForm
    
    def get_context_data(self, **kwargs):
        context = super(EmployeeAdd, self).get_context_data(**kwargs)
        context['add_employee_form'] = self.get_form()
        return context

    def form_valid(self, form):
        add_employee_form = form.save()
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


class ProjectList(LoginRequiredMixin, ListView):
    model = Projects
    template_name = 'employees/projectlist.html'
    context_object_name = 'project_list'


class Dashboard(ListView):
    model = Employee
    template_name = 'employees/dashboard.html'
    context_object_name = 'dashboard'

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['add_employee_form'] = EmployeeAddForm
        context['project_form'] = AddProject
        context['employees_list'] = Employee.objects.all()
        context['project_list'] = Projects.objects.all()
        return context


class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Projects
    template_name = 'employees/projectdetails.html'
    context_object_name = 'project_detail'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['task'] = Task.objects.filter(project=self.object.id)
        return context


class EmployeeProjects(LoginRequiredMixin, FormView):
    model = Projects
    template_name = 'employees/project.html'
    success_url = reverse_lazy('employees:dashboard')
    form_class = AddProject
    
    def get_context_data(self, **kwargs):
        context = super(EmployeeProjects, self).get_context_data(**kwargs)
        context['project_form'] = self.get_form()
        return context

    def form_valid(self, form):
        project_form = form.save()
        return super(EmployeeProjects, self).form_valid(form)


class ProjectDelete(DeleteView):
    model = Projects
    template_name = 'employees/delete.html'

    def get_success_url(self):
        return reverse_lazy('employees:dashboard')


class EmployeeDelete(DeleteView):
    model = Employee
    success_url = reverse_lazy('employees:dashboard')
    template_name = 'employees/remove.html'


class TaskList(FormView):
    model = Task
    template_name = 'employees/task.html'
    form_class = AddTask

    def get_context_data(self, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)
        context['task'] = self.get_form()
        return context

    def get_success_url(self):
        return reverse_lazy('employees:project_detail', args=(self.kwargs['pk'],))

    def form_valid(self, form):
        task = form.save(commit=False)
        task.project = Projects.objects.get(id=self.kwargs['pk'])
        task.save()
        return super(TaskList, self).form_valid(form)
