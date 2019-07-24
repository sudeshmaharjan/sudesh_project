from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
import datetime

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255)
    email = models.EmailField( unique=True)
    phone = models.BigIntegerField()
    qualification = models.CharField(max_length=255)
    about = models.TextField(max_length=500, blank=True, default='N/A')
    pic = models.ImageField(max_length=255, upload_to='profile', default='profile/default.png')

    def __str__(self):
        return self.first_name


class Experience(models.Model):
    experience_fields = models.CharField(max_length=255)
    experience_years = models.IntegerField()
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'experience'


class Projects(models.Model):
    project_title = models.CharField(max_length=255, unique=True)
    client_name = models.CharField(max_length=255)
    project_description = models.FileField(blank=True, null=True, upload_to="projects", validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    project_begin = models.DateField(default=datetime.date.today)

    class Meta:
        db_table = 'employees_projects'

    def __str__(self):
        return self.project_title

    
class Task(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, blank=True, null=True)
    start_dt = models.DateTimeField(default=datetime.datetime.now)
    end_dt = models.DateTimeField(blank=True, null=True)
    task_name = models.CharField(max_length=255, blank=True, null=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.SET_NULL, related_name='task', blank=True, null=True)
    is_completed = models.BooleanField(default=False)


class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(null=True, blank=True, max_length=255)
    qualification = models.CharField(max_length=255)
    about = models.TextField(max_length=500, blank=True, default='N/A')
    pic = models.ImageField(max_length=255, upload_to='profile', default='profile/default.png')

    def __str__(self):
        return f"Account of {self.user.first_name}"