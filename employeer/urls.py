from django.conf.urls import url
from .views import EmployeerName, EmployeerDetail, EmployeerUpdate


app_name = "employeer"

urlpatterns = [
    url(r"^$",EmployeerName.as_view(), name="employeer"),
    url(r"^employeer/(?P<pk>\d+)/$", EmployeerDetail.as_view(), name="employeer_detail"),
    url(r"edit/(?P<pk>\d+)/$", EmployeerUpdate.as_view(), name="edit"),
]