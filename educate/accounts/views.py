from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from . models import User, School
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView
from django.views.generic.detail import DetailView
from .forms import UserForm, SchoolForm

# Create your views here.
@login_required
def home(request):
    user = request.user
    name = user.first_name + " " + user.last_name
    args = {'name': name}
    if user.user_type == 1: # tutor
        return render(request, 'tutor/tutor.html', args)
    elif user.user_type == 2: # tech
        return render(request, 'tech/tech.html', args)
    elif user.user_type == 3: # tutor_leader
        return render(request, 'tutor_leader/tutor_leader.html', args)
    elif user.user_type == 4: # tech_leader
        return render(request, 'tech_leader/tech_leader.html', args)

@login_required
class UserCreate(CreateView):
    model = User
    template_name = 'tech_leader/user/form.html'
    form_class = UserForm
    success_url = reverse_lazy('accounts:user_list')

@login_required
class UserList(ListView):
    queryset = User.objects.order_by('id')
    template_name = 'tech_leader/user/list.html'

@login_required
class UserUpdate(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'tech_leader/user/form.html'
    success_url = reverse_lazy('accounts:user_list')

@login_required
class UserDelete(DeleteView):
    model = User
    template_name = 'tech_leader/user/delete.html'
    success_url = reverse_lazy('accounts:user_list')

@login_required
class UserShow(DetailView):
    model = User
    template_name = 'tech_leader/user/show.html'

@login_required
class SchoolCreate(CreateView):
    model = School
    template_name = 'tech_leader/school/form.html'
    form_class = SchoolForm
    success_url = reverse_lazy('accounts:school_list')

@login_required
class SchoolList(ListView):
    queryset = School.objects.order_by('id')
    template_name = 'tech_leader/school/list.html'

@login_required
class SchoolUpdate(UpdateView):
    model = School
    form_class = SchoolForm
    template_name = 'tech_leader/school/form.html'
    success_url = reverse_lazy('accounts:school_list')

@login_required
class SchoolDelete(DeleteView):
    model = School
    template_name = 'tech_leader/school/delete.html'
    success_url = reverse_lazy('accounts:school_list')

@login_required
class SchoolShow(DetailView):
    model = School
    template_name = 'tech_leader/school/show.html'
