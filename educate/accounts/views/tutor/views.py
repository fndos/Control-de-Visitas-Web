from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import connection
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView
from django.views.generic.detail import DetailView
from django.db.models import Q

from ... models import Requirement, Visit
from ... forms import VisitCreateForm, VisitUpdateForm, RequirementCreateForm
from ... decorators import tutor_required

############################    Requirement    #################################

@method_decorator([login_required, tutor_required], name='dispatch')
class RequirementList(TemplateView):
    template_name = 'tutor/requirement/list.html'

    def get_context_data(self, **kwargs):
        context = super(RequirementList, self).get_context_data(**kwargs)
        try:
            context['object_requirement'] = Requirement.objects.filter(~Q(type=None) & Q(type=3) & Q(user=self.request.user))
        except Visit.DoesNotExist:
            context['object_requirement'] = None
        return context

@method_decorator([login_required, tutor_required], name='dispatch')
class RequirementShow(DetailView):
    model = Requirement
    template_name = 'tutor/requirement/show.html'

##############################    Visit    #####################################

############################    Planning    ####################################
