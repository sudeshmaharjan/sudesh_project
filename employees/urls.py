from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from employees import views
from .views import (
    EmployeeList, EmployeeDetail, EmployeeUpdate, EmployeeAdd, EmployeeDelete, UserProfile, TaskEdit, TaskDelete, IsComplete,
    EmployeeExperience, ProjectList, ProjectDetail, EmployeeProjects, ProjectDelete, Dashboard, TaskList, TaskComplete, ProjectEdit
)


app_name = "employees"

urlpatterns = [
    url(r"^add/$", EmployeeAdd.as_view(), name="new"),
    url(r"^$", EmployeeList.as_view(), name="employees_list"),
    url(r"^employee/(?P<pk>\d+)/$", EmployeeDetail.as_view(), name="employees_detail"),
    url(r"^employee/(?P<pk>\d+)/experience/$", EmployeeExperience.as_view(), name="experience"),
    url(r"^profile/(?P<slug>\w+)/edit/$", EmployeeUpdate.as_view(), name="edit"),
    url(r"^remove/(?P<pk>\d+)/$", EmployeeDelete.as_view(), name="remove"),
    url(r"^project/$", EmployeeProjects.as_view(), name="projects"),
    url(r"^projects/$", ProjectList.as_view(), name="project_list"),
    url(r"^projects/(?P<pk>\d+)/$", ProjectDetail.as_view(), name="project_detail"),
    url(r"^projects/(?P<pk>\d+)/delete/$", ProjectDelete.as_view(), name="delete"),
    url(r"^projects/(?P<pk>\d+)/task/$", TaskList.as_view(), name="task"),
    url(r"^projects/(?P<pk>\d+)/edit/$", ProjectEdit.as_view(), name="projectedit"),
    url(r"^projects/(?P<project>\d+)/task/(?P<pk>\d+)/edit/$", TaskEdit.as_view(), name="taskedit"),
    url(r"^projects/(?P<project>\d+)/task/(?P<pk>\d+)/delete/$", TaskDelete.as_view(), name="taskdel"),
    url(r"^profile/task/(?P<pk>\d+)/complete/$", TaskComplete.as_view(), name="taskcomplete"),
    url(r"^task/(?P<pk>\d+)/iscomplete/$", IsComplete.as_view(), name="iscomplete"),
    url(r"^dashboard/$", Dashboard.as_view(), name="dashboard"),
    url(r"^profile/$", UserProfile.as_view(), name="profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)