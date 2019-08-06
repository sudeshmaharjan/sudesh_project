from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from .models import Employee, Experience, Projects, Task
from django.views.generic import ListView, DetailView, TemplateView
from django.urls import reverse_lazy, reverse
from .forms import EmployeeAddForm, AddExperience, ExperienceFormSet, AddProject, AddTask
from django.views.generic.edit import DeleteView, FormView, UpdateView
from django.db import transaction
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.base import ObjectDoesNotExist


class EmployeeList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employees/list.html'
    context_object_name = 'employees_list'
    permission_required = ('user.is_superuser',)


class EmployeeDetail(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'employees/details.html'
    context_object_name = 'employees_detail'
    permission_required = ('user.is_superuser',)

    def get_context_data(self, **kwargs):
        context = super(EmployeeDetail, self).get_context_data(**kwargs)
        context['experience'] = Experience.objects.filter(employee_id=self.object.id)
        # context['projects'] = Projects.objects.filter(employee_id=self.object.id)
        context['task'] = Task.objects.filter(employee_id=self.object.id)
        return context


class UserProfile(LoginRequiredMixin, TemplateView):
    template_name = 'employees/profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        # user = self.request.user
        # employeee = Employee.objects.filter(user__username=self.request.user.username)
        # if user in employeee:
        #     print(user)
        # else:
        #     print('no profile')
        # employee_set = Employee.objects.all()
        # print(employee_set)       
        # print(employeee)
        # print(self.request.user)       
        try:
            employee = Employee.objects.get(user__username=self.request.user.username)
            context['experience'] = Experience.objects.filter(employee_id=employee.id)
            # context['projects'] = Projects.objects.filter(employee_id=self.object.id)
            context['task'] = Task.objects.filter(employee_id=employee.id)
            context['tsk_form'] = AddTask
            context['employees_detail'] = employee
            return context

        except ObjectDoesNotExist:
            return
        

class EmployeeAdd(PermissionRequiredMixin, LoginRequiredMixin, FormView):
    model = Employee
    template_name = 'employees/new.html'
    success_url = reverse_lazy('employees:dashboard')
    form_class = EmployeeAddForm
    permission_required = ('user.is_superuser',)
    
    def get_context_data(self, **kwargs):
        context = super(EmployeeAdd, self).get_context_data(**kwargs)
        context['add_employee_form'] = self.get_form()
        return context

    def form_valid(self, form):
        add_employee_form = form.save()
        return super(EmployeeAdd, self).form_valid(form)


class EmployeeUpdate(LoginRequiredMixin, UpdateView):
    model = Employee
    template_name = 'employees/edit.html'
    form_class = EmployeeAddForm
    slug_field = 'user__username'

    def get_success_url(self):
        if self.request.method=='POST' and 'btn_exit' in self.request.POST:
            return reverse_lazy('employees:profile',)
        if self.request.method == 'POST' and 'btn_update' in self.request.POST:
            return reverse_lazy('employees:edit', args=(self.object.user.username,))

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

    
class EmployeeExperience(LoginRequiredMixin, FormView):
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


class ProjectList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Projects
    template_name = 'employees/projectlist.html'
    context_object_name = 'project_list'
    permission_required = ('user.is_superuser',)


class Dashboard(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employees/dashboard.html'
    context_object_name = 'dashboard'
    permission_required = ('user.is_superuser',)

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        employee = Employee.objects.get(user__username=self.request.user.username)
        context['detail'] = Employee.objects.get(user__username=self.request.user.username)
        context['add_employee_form'] = EmployeeAddForm
        context['project_form'] = AddProject
        context['employees_list'] = Employee.objects.all()
        context['project_list'] = Projects.objects.all()
        return context


class ProjectDetail(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = Projects
    template_name = 'employees/projectdetails.html'
    context_object_name = 'project_detail'
    permission_required = ('user.is_superuser',)

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['task'] = Task.objects.filter(project=self.object.id)
        return context


class EmployeeProjects(PermissionRequiredMixin, LoginRequiredMixin, FormView):
    model = Projects
    template_name = 'employees/project.html'
    success_url = reverse_lazy('employees:dashboard')
    form_class = AddProject
    permission_required = ('user.is_superuser',)
    
    def get_context_data(self, **kwargs):
        context = super(EmployeeProjects, self).get_context_data(**kwargs)
        context['project_form'] = self.get_form()
        return context

    def form_valid(self, form):
        project_form = form.save()
        return super(EmployeeProjects, self).form_valid(form)


class ProjectEdit(UpdateView):
    model = Projects
    template_name = 'employees/projectedit.html'
    form_class = AddProject

    def get_context_data(self, **kwargs):
        context = super(ProjectEdit, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy('employees:project_detail', args=(self.kwargs['pk'],))

    def form_valid(self, form):
        form.save()
        return super(ProjectEdit, self).form_valid(form)


class ProjectDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Projects
    template_name = 'employees/delete.html'
    permission_required = ('user.is_superuser',)

    def get_success_url(self):
        return reverse_lazy('employees:dashboard')


class EmployeeDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Employee
    success_url = reverse_lazy('employees:dashboard')
    template_name = 'employees/remove.html'
    permission_required = ('user.is_superuser',)


class TaskList(PermissionRequiredMixin, LoginRequiredMixin, FormView):
    model = Task
    template_name = 'employees/task.html'
    form_class = AddTask
    permission_required = ('user.is_superuser',)

    def get_success_url(self):
        return reverse_lazy('employees:project_detail', args=(self.kwargs['pk'],))

    def form_valid(self, form):
        task = form.save(commit=False)
        task.project = Projects.objects.get(id=self.kwargs['pk'])
        task.save()
        return super(TaskList, self).form_valid(form)

class TaskEdit(UpdateView):
    model = Task
    template_name = 'employees/taskedit.html'
    form_class = AddTask

    def get_context_data(self, **kwargs):
        context = super(TaskEdit, self).get_context_data(**kwargs)
        context['taskedit'] = self.get_form()
        return context

    def get_success_url(self):
        return reverse_lazy('employees:project_detail', args=(self.kwargs['project'],))

    def form_valid(self, form):
        taskedit = form.save(commit=False)
        taskedit.project = Projects.objects.get(id=self.kwargs['project'])
        taskedit.save()
        return super(TaskEdit, self).form_valid(form)

class TaskDelete(DeleteView):
    model = Task
    template_name = 'employees/taskdelete.html'
    
    def get_success_url(self):
        return reverse_lazy('employees:project_detail', args=(self.kwargs['project'],))

class TaskComplete(UpdateView):
    model = Task
    template_name = 'employees/taskcomplete.html'
    form_class = AddTask
    success_url = reverse_lazy('employees:profile')

    def get_context_data(self, **kwargs):
        context = super(TaskComplete, self).get_context_data(**kwargs)
        context['taskcomplete'] = self.object.id
        context['task'] = AddTask
        return context

    def form_valid(self, form):
        form.save()
        return super(TaskComplete, self).form_valid(form)
    

class IsComplete(TemplateView):
    template_name = 'employees/iscomplete.html'

    def dispatch(self, request, *args, **kwargs):
        obj = Task.objects.get(id=self.kwargs['pk'])
        if obj.is_completed:
            obj.is_completed = False
        else:
            obj.is_completed = True
        obj.save()
        return HttpResponseRedirect(reverse_lazy('employees:profile'))
        






# @login_required
# def profile(request):
#     return render(request, "employees/profile.html")