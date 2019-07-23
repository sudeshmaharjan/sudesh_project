from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Employee, Experience, Projects, Task
from django import forms


class ExperienceInline(admin.TabularInline):
    model = Experience
    fk_name = "employee_id"

class EmployeeAdmin(admin.ModelAdmin):
    inlines = [
        ExperienceInline,
    ]

class TaskInline(admin.TabularInline):
    model = Task
    fk_name = "project"

class ProjectAdmin(admin.ModelAdmin):
    model = Projects
    fk_name = "employee_id"
    inlines = [
       TaskInline,
    ]

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Projects,ProjectAdmin)
