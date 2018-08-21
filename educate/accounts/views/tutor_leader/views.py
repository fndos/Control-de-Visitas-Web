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
from ... decorators import tutor_leader_required

############################    Requirement    #################################

@method_decorator([login_required, tutor_leader_required], name='dispatch')
class RequirementCreate(CreateView):
    model = Visit
    template_name = 'tutor_leader/planning/form.html'
    form_class = RequirementCreateForm
    success_url = reverse_lazy('accounts:planning_visit_create')

    def form_valid(self, form):
        form.instance.created_by = str(self.request.user)
        form.instance.user_id = self.request.user.id
        return super(RequirementCreate, self).form_valid(form)

@method_decorator([login_required, tutor_leader_required], name='dispatch')
class RequirementList(TemplateView):
    template_name = 'tutor_leader/requirement/list.html'

    def get_context_data(self, **kwargs):
        context = super(RequirementList, self).get_context_data(**kwargs)
        try: 
            context['object_requirement'] = Requirement.objects.filter(~Q(type=None) & Q(type=3) & Q(user=self.request.user))
        except Visit.DoesNotExist:
            context['object_requirement'] = None
        return context

@method_decorator([login_required, tutor_leader_required], name='dispatch')
class RequirementUpdate(UpdateView):
    model = Requirement
    form_class = RequirementCreateForm
    template_name = 'tutor_leader/planning/form.html'

    def get_success_url(self):
        visit = Visit.objects.get(requirement=self.kwargs['pk'])
        return reverse_lazy('accounts:planning_visit_update', kwargs={'pk': visit.id})

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

@method_decorator([login_required, tutor_leader_required], name='dispatch')
class RequirementShow(DetailView):
    model = Requirement
    template_name = 'tutor_leader/requirement/show.html'

##############################    Visit    #####################################

@method_decorator([login_required, tutor_leader_required], name='dispatch')
class VisitCreate(CreateView):
    model = Visit
    template_name = 'tutor_leader/planning/next.html'
    form_class = VisitCreateForm
    success_url = reverse_lazy('accounts:planning_list')

    def form_valid(self, form):
        form.instance.created_by = str(self.request.user)
        return super(VisitCreate, self).form_valid(form)

@method_decorator([login_required, tutor_leader_required], name='dispatch')
class VisitList(TemplateView):
    template_name = 'tutor_leader/visit/list.html'

    def get_context_data(self, **kwargs):
        context = super(VisitList, self).get_context_data(**kwargs)
        try:
            context['object_visit'] = Visit.objects.filter(Q(requirement__type=None))
        except Visit.DoesNotExist:
            context['object_visit'] = None
        return context

@method_decorator([login_required, tutor_leader_required], name='dispatch')
class VisitUpdate(UpdateView):
    model = Visit
    form_class = VisitUpdateForm
    template_name = 'tutor_leader/planning/next.html'
    success_url = reverse_lazy('accounts:planning_list')

    def form_valid(self, form):
        form.instance.updated_by = str(self.request.user)
        return super(VisitUpdate, self).form_valid(form)

@method_decorator([login_required, tutor_leader_required], name='dispatch')
class VisitDelete(DeleteView):
    model = Requirement
    template_name = 'tutor_leader/planning/delete.html'
    success_url = reverse_lazy('accounts:planning_list')

@method_decorator([login_required, tutor_leader_required], name='dispatch')
class VisitShow(DetailView):
    model = Visit
    template_name = 'tutor_leader/planning/show.html'

@method_decorator([login_required, tutor_leader_required], name='dispatch')
class VisitDetail(DetailView):
    model = Visit
    template_name = 'tutor_leader/visit/show.html'

############################    Planning    ####################################

@method_decorator([login_required, tutor_leader_required], name='dispatch')
class PlanningList(TemplateView):
    template_name = 'tutor_leader/planning/list.html'

    def get_context_data(self, **kwargs):
        context = super(PlanningList, self).get_context_data(**kwargs)
        try:
            context['object_visit'] = Visit.objects.filter(user=self.request.user).order_by('date_planned')
        except Visit.DoesNotExist:
            context['object_visit'] = None
        return context