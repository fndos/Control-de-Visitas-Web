from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import connection
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.http import JsonResponse
from django.core.serializers import serialize
from datetime import datetime
import json

from ... models import Requirement, Visit, TechnicalForm, PedagogicalForm
from ... forms import VisitCreateTutorForm, VisitUpdateTutorForm, RequirementCreateForm
from ... decorators import tutor_required

@login_required
def LoginRedirect(request):
    user = request.user
    args = {'test': user}
    if user.user_type == 1: # tutor
        return HttpResponseRedirect('/accounts/nr/planning/')
    elif user.user_type == 2: # tech
        return HttpResponseRedirect('/accounts/nt/planning/')
    elif user.user_type == 3: # tutor_leader
        return HttpResponseRedirect('/accounts/r/planning/')
    elif user.user_type == 4: # tech_leader
        return HttpResponseRedirect('/accounts/t/users/')

############################    Requirement    #################################

@method_decorator([login_required, tutor_required], name='dispatch')
class RequirementCreate(CreateView):
    model = Visit
    template_name = 'tutor/planning/form.html'
    form_class = RequirementCreateForm
    success_url = reverse_lazy('accounts:planning_visit_create_tutor')

    def form_valid(self, form):
        form.instance.created_by = str(self.request.user)
        form.instance.user_id = self.request.user.id
        return super(RequirementCreate, self).form_valid(form)

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
class RequirementUpdate(UpdateView):
    model = Requirement
    form_class = RequirementCreateForm
    template_name = 'tutor/planning/form.html'

    def get_success_url(self):
        visit = Visit.objects.get(requirement=self.kwargs['pk'])
        return reverse_lazy('accounts:planning_visit_update_tutor', kwargs={'pk': visit.id})

    def get_context_data(self, **kwargs):
        context = super(RequirementUpdate, self).get_context_data(**kwargs)
        try:
            context['object_visit'] = Visit.objects.get(requirement__id=self.kwargs['pk'])
        except Visit.DoesNotExist:
            context['object_visit'] = None
        return context

    def form_valid(self, form):
        form.instance.updated_by = str(self.request.user)
        form.instance.user_id = self.request.user.id
        return super(RequirementUpdate, self).form_valid(form)

@method_decorator([login_required, tutor_required], name='dispatch')
class RequirementShow(DetailView):
    model = Requirement
    template_name = 'tutor/requirement/show.html'

##############################    Visit    #####################################

@method_decorator([login_required, tutor_required], name='dispatch')
class VisitCreate(CreateView):
    model = Visit
    template_name = 'tutor/planning/next.html'
    form_class = VisitCreateTutorForm
    success_url = reverse_lazy('accounts:planning_list_tutor')

    def get_form_kwargs(self):
        kw = super(VisitCreate, self).get_form_kwargs()
        kw['request'] = self.request # the trick!
        return kw

    def form_valid(self, form):
        form.instance.created_by = str(self.request.user)
        return super(VisitCreate, self).form_valid(form)

@method_decorator([login_required, tutor_required], name='dispatch')
class VisitUpdate(UpdateView):
    model = Visit
    form_class = VisitUpdateTutorForm
    template_name = 'tutor/planning/next.html'
    success_url = reverse_lazy('accounts:planning_list_tutor')

    def get_form_kwargs(self):
        kw = super(VisitUpdate, self).get_form_kwargs()
        kw['request'] = self.request # the trick!
        return kw

    def form_valid(self, form):
        form.instance.updated_by = str(self.request.user)
        return super(VisitUpdate, self).form_valid(form)

@method_decorator([login_required, tutor_required], name='dispatch')
class VisitDelete(DeleteView):
    model = Requirement
    template_name = 'tutor/planning/delete.html'
    success_url = reverse_lazy('accounts:planning_list_tutor')

    def get_context_data(self, **kwargs):
        context = super(VisitDelete, self).get_context_data(**kwargs)
        try:
            context['object_visit'] = Visit.objects.get(requirement__id=self.kwargs['pk'])
        except Visit.DoesNotExist:
            context['object_visit'] = None
        return context

@method_decorator([login_required, tutor_required], name='dispatch')
class VisitShow(DetailView):
    model = Visit
    template_name = 'tutor/planning/show.html'

    def get_context_data(self, **kwargs):
        context = super(VisitShow, self).get_context_data(**kwargs)
        try:
            #obtener información de los formularios
            context['object_technical_form'] = TechnicalForm.objects.filter(Q(id=self.kwargs['pk']))
            context['object_pedagogical_form'] = PedagogicalForm.objects.filter(Q(id=self.kwargs['pk']))
            print(context['object_pedagogical_form'])
        except TechnicalForm.DoesNotExist:
            context['object_technical_form'] = None
        except  PedagogicalForm.DoesNotExist:
            context['object_pedagogical_form'] = None
        return context

############################    Planning    ####################################

@method_decorator([login_required, tutor_required], name='dispatch')
class PlanningList(TemplateView):
    template_name = 'tutor/planning/list.html'

    def get_context_data(self, **kwargs):
        context = super(PlanningList, self).get_context_data(**kwargs)
        date_planned = datetime.now()
        date_planned = date_planned.strftime("%Y-%m-%d")
        try:
            context['object_visit'] = Visit.objects.filter(Q(user=self.request.user) & Q(date_planned__contains=date_planned)).order_by('date_planned')
            query_set = Visit.objects.filter(Q(user=self.request.user)).order_by('date_planned')
            data = []
            for visit in query_set:
                data.append(str(visit.date_planned.date()))
            context['data'] = list(set(data))
            print(list(set(data)))
        except Visit.DoesNotExist:
            context['object_visit'] = None
            context['data'] = None
        return context

@login_required
def ItemUpdate(request):
    try:
        query_set = Visit.objects.filter(Q(user=request.user) & Q(date_planned__contains=request.GET.get('date_planned'))).order_by('date_planned')
    except Visit.DoesNotExist:
        query_set = None
    return render(request, 'tutor/planning/items.html', {'object_visit':query_set})
