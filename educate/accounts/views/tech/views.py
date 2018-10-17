from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import connection
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView
from django.views.generic.detail import DetailView
from django.db.models import Q
from datetime import datetime

from ... models import User, School, Requirement, Visit, TechnicalForm, PedagogicalForm
from ... forms import UserForm, SchoolForm, RequirementForm, VisitForm
from ... decorators import tech_required

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

##############################    Visit    #####################################

@method_decorator([login_required, tech_required], name='dispatch')
class VisitShow(DetailView):
    model = Visit
    template_name = 'tech/planning/show.html'

    def get_context_data(self, **kwargs):
        context = super(VisitShow, self).get_context_data(**kwargs)
        try:
            #obtener información de los formularios
            context['object_technical_form'] = TechnicalForm.objects.filter(Q(visit=self.kwargs['pk']))
            context['object_pedagogical_form'] = PedagogicalForm.objects.filter(Q(visit=self.kwargs['pk']))
            print(context['object_pedagogical_form'])
        except TechnicalForm.DoesNotExist:
            context['object_technical_form'] = None
        except  PedagogicalForm.DoesNotExist:
            context['object_pedagogical_form'] = None
        return context

############################    Planning    ####################################

@method_decorator([login_required, tech_required], name='dispatch')
class PlanningList(TemplateView):
    template_name = 'tech/planning/list.html'

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
    return render(request, 'tech/planning/items.html', {'object_visit':query_set})
