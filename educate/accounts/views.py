from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import connection
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView
from django.views.generic.detail import DetailView

from . models import User, School, Requirement, Visit
from .forms import UserForm, SchoolForm, RequirementForm, VisitForm
from . decorators import tech_leader_required

@login_required
def LoginRedirect(request):
    user = request.user
    args = {'test': user}
    if user.user_type == 1: # tutor
        return render(request, 'tutor/home.html', args)
    elif user.user_type == 2: # tech
        return render(request, 'tech/home.html', args)
    elif user.user_type == 3: # tutor_leader
        return render(request, 'tutor_leader/home.html', args)
    elif user.user_type == 4: # tech_leader
        return render(request, 'tech_leader/home.html', args)

##############################    Users    #####################################

@method_decorator([login_required, tech_leader_required], name='dispatch')
class UserCreate(CreateView):
    model = User
    template_name = 'tech_leader/user/form.html'
    form_class = UserForm
    success_url = reverse_lazy('accounts:user_list')

@method_decorator([login_required, tech_leader_required], name='dispatch')
class UserList(ListView):
    queryset = User.objects.order_by('id')
    template_name = 'tech_leader/user/list.html'

@method_decorator([login_required, tech_leader_required], name='dispatch')
class UserUpdate(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'tech_leader/user/form.html'
    success_url = reverse_lazy('accounts:user_list')

@method_decorator([login_required, tech_leader_required], name='dispatch')
class UserDelete(DeleteView):
    model = User
    template_name = 'tech_leader/user/delete.html'
    success_url = reverse_lazy('accounts:user_list')

@method_decorator([login_required, tech_leader_required], name='dispatch')
class UserShow(DetailView):
    model = User
    template_name = 'tech_leader/user/show.html'

##############################    School    ####################################

@method_decorator([login_required, tech_leader_required], name='dispatch')
class SchoolCreate(CreateView):
    model = School
    template_name = 'tech_leader/school/form.html'
    form_class = SchoolForm
    success_url = reverse_lazy('accounts:school_list')
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(SchoolCreate, self).form_valid(form)

@method_decorator([login_required, tech_leader_required], name='dispatch')
class SchoolList(ListView):
    queryset = School.objects.order_by('id')
    template_name = 'tech_leader/school/list.html'

@method_decorator([login_required, tech_leader_required], name='dispatch')
class SchoolUpdate(UpdateView):
    model = School
    form_class = SchoolForm
    template_name = 'tech_leader/school/form.html'
    success_url = reverse_lazy('accounts:school_list')

@method_decorator([login_required, tech_leader_required], name='dispatch')
class SchoolDelete(DeleteView):
    model = School
    template_name = 'tech_leader/school/delete.html'
    success_url = reverse_lazy('accounts:school_list')

@method_decorator([login_required, tech_leader_required], name='dispatch')
class SchoolShow(DetailView):
    model = School
    template_name = 'tech_leader/school/show.html'

##############################    Visit    #####################################
@method_decorator([login_required, tech_leader_required], name='dispatch')
class VisitCreate(CreateView):
    model = Visit
    template_name = 'tech_leader/visit/form.html'
    form_class = VisitForm
    success_url = reverse_lazy('accounts:visit_list')

@method_decorator([login_required, tech_leader_required], name='dispatch')
class VisitList(TemplateView):
    template_name = 'tech_leader/visit/list.html'

    def get_context_data(self, **kwargs):
        context = super(VisitList, self).get_context_data(**kwargs)
        context['object_list'] = Visit.objects.order_by('id')
        context['object_requirement'] = Requirement.objects.all()
        context['object_school'] = School.objects.all()
        return context

@method_decorator([login_required, tech_leader_required], name='dispatch')
class VisitUpdate(UpdateView):
    model = Visit
    form_class = VisitForm
    template_name = 'tech_leader/visit/form.html'
    success_url = reverse_lazy('accounts:visit_list')

@method_decorator([login_required, tech_leader_required], name='dispatch')
class VisitDelete(DeleteView):
    model = Visit
    template_name = 'tech_leader/visit/delete.html'
    success_url = reverse_lazy('accounts:visit_list')

@method_decorator([login_required, tech_leader_required], name='dispatch')
class VisitShow(DetailView):
    model = Visit
    template_name = 'tech_leader/visit/show.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(VisitShow, self).get_context_data(**kwargs)
        # Add extra context from another model
        context['object_requirement'] = Requirement.objects.all()
        context['object_school'] = School.objects.all()
        return context

#############################  Requirement  ####################################

@method_decorator([login_required, tech_leader_required], name='dispatch')
class RequirementCreate(CreateView):
    model = Requirement
    template_name = 'tech_leader/requirement/form.html'
    form_class = RequirementForm
    success_url = reverse_lazy('accounts:requirement_list')
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.user_id = self.request.user.id
        return super(RequirementCreate, self).form_valid(form)

@method_decorator([login_required, tech_leader_required], name='dispatch')
class RequirementList(ListView):
    queryset = Requirement.objects.order_by('id')
    template_name = 'tech_leader/requirement/list.html'

@method_decorator([login_required, tech_leader_required], name='dispatch')
class RequirementUpdate(UpdateView):
    model = Requirement
    form_class = RequirementForm
    template_name = 'tech_leader/requirement/form.html'
    success_url = reverse_lazy('accounts:requirement_list')

@method_decorator([login_required, tech_leader_required], name='dispatch')
class RequirementDelete(DeleteView):
    model = Requirement
    template_name = 'tech_leader/requirement/delete.html'
    success_url = reverse_lazy('accounts:requirement_list')

@method_decorator([login_required, tech_leader_required], name='dispatch')
class RequirementShow(DetailView):
    model = Requirement
    template_name = 'tech_leader/requirement/show.html'
