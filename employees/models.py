from django.db import models
from django.core.validators import FileExtensionValidator
import datetime

class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.BigIntegerField()
    qualification = models.CharField(max_length=255)
    about = models.TextField(max_length=500, blank=True, default='N/A')
    pic = models.ImageField(max_length=255, blank=True, null=True, upload_to='profile')

    def __str__(self):
        return self.first_name


class Experience(models.Model):
    experience_fields = models.CharField(max_length=255)
    experience_years = models.IntegerField()
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'experience'


class Projects(models.Model):
    project_title = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)
    project_description = models.FileField(blank=True, null=True, upload_to="projects", validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    project_begin = models.DateField()
    employee_id = models.ForeignKey(Employee, related_name="project", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'employees_projects'