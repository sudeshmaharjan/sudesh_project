from django.contrib import admin
from .models import Employee, Experience, Projects


class ExperienceInline(admin.TabularInline):
    model = Experience
    fk_name = "employee_id"

class ProjectInline(admin.TabularInline):
    model = Projects
    fk_name = "employee_id"

class EmployeeAdmin(admin.ModelAdmin):
    inlines = [
        ExperienceInline,
        ProjectInline,
    ]
    

admin.site.register(Employee, EmployeeAdmin)
