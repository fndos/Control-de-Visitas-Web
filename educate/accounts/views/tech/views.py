from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import connection
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView
from django.views.generic.detail import DetailView
from django.db.models import Q

from ... models import User, School, Requirement, Visit
from ... forms import UserForm, SchoolForm, RequirementForm, VisitForm
from ... decorators import tech_required

##############################    Visit    #####################################

@method_decorator([login_required, tech_required], name='dispatch')
class VisitList(TemplateView):
    template_name = 'tech/visit/list.html'
    #  ~Q(requirement__type=None) Visualizar sólo visitas Técnicas
    def get_context_data(self, **kwargs):
        context = super(VisitList, self).get_context_data(**kwargs)
        try:
            context['object_visit'] = Visit.objects.filter(user=self.request.user and ~Q(requirement__type=None))
        except Visit.DoesNotExist:
            context['object_visit'] = None
        return context

@method_decorator([login_required, tech_required], name='dispatch')
class VisitShow(DetailView):
    model = Visit
    template_name = 'tech/visit/show.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(VisitShow, self).get_context_data(**kwargs)
        # Add extra context from another model
        context['object_requirement'] = Requirement.objects.all()
        context['object_school'] = School.objects.all()
        return context
