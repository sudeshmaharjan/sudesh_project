from django.shortcuts import render
from .models import Employeer
from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse_lazy


class EmployeerName(ListView):
    model = Employeer
    template_name = 'employeer/employeer.html'
    context_object_name = 'employeer'


class EmployeerDetail(DetailView):
    model = Employeer
    template_name = 'employeer/detail.html'
    context_object_name = 'employeer_detail'


class EmployeerUpdate(UpdateView):
    model = Employeer
    template_name = 'employeer/edit.html'
    fields = '__all__'
    success_url = reverse_lazy('employeer:employeer')