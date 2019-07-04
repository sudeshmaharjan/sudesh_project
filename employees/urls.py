from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from .views import EmployeeList, EmployeeDetail, EmployeeUpdate, EmployeeAdd, EmployeeDelete, EmployeeExperience, EmployeeProjects


app_name = "employees"

urlpatterns = [
    url(r"^$", EmployeeList.as_view(), name="employees_list"),
    url(r"^add/$", EmployeeAdd.as_view(), name='new'),
    url(r"^employee/(?P<pk>\d+)/$", EmployeeDetail.as_view(), name="employees_detail"),
    url(r"^edit/(?P<pk>\d+)/$", EmployeeUpdate.as_view(), name="edit"),
    url(r"^employee/(?P<pk>\d+)/experience/$", EmployeeExperience.as_view(), name="experience"),
    url(r"^employee/(?P<pk>\d+)/projects/$", EmployeeProjects.as_view(), name="projects"),   
    url(r"^remove/(?P<pk>\d+)/$", EmployeeDelete.as_view(), name="remove"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)