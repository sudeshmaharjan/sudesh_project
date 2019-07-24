from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from employees import views
from .views import (
    EmployeeList, EmployeeDetail, EmployeeUpdate, EmployeeAdd, EmployeeDelete, UserProfile,
    EmployeeExperience, ProjectList, ProjectDetail, EmployeeProjects, ProjectDelete, Dashboard, TaskList
)


app_name = "employees"

urlpatterns = [
    url(r"^add/$", EmployeeAdd.as_view(), name="new"),
    url(r"^$", EmployeeList.as_view(), name="employees_list"),
    url(r"^employee/(?P<pk>\d+)/$", EmployeeDetail.as_view(), name="employees_detail"),
    url(r"^employee/(?P<pk>\d+)/experience/$", EmployeeExperience.as_view(), name="experience"),
    url(r"^edit/(?P<pk>\d+)/$", EmployeeUpdate.as_view(), name="edit"),
    url(r"^remove/(?P<pk>\d+)/$", EmployeeDelete.as_view(), name="remove"),
    url(r"^project/$", EmployeeProjects.as_view(), name="projects"),
    url(r"^projects/$", ProjectList.as_view(), name="project_list"),
    url(r"^projects/(?P<pk>\d+)/$", ProjectDetail.as_view(), name="project_detail"),
    url(r"^projects/(?P<pk>\d+)/delete/$", ProjectDelete.as_view(), name="delete"),
    url(r"^projects/(?P<pk>\d+)/task/$", TaskList.as_view(), name="task"),
    url(r"^dashboard/$", Dashboard.as_view(), name="dashboard"),
    url(r"^profile/$", UserProfile.as_view(), name="profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)