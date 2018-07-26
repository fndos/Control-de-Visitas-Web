from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from . decorators import tutor_required

from . models import User
from django.views.generic import TemplateView

# Create your views here.
@login_required
def home(request):
    user = request.user
    name = user.first_name + " " + user.last_name
    args = {'name': name}
    if user.is_tutor and not user.is_leader:
        # tutor
        return render(request, 'tutor/tutor.html', args)
    elif user.is_tutor and user.is_leader:
        # tutor_leader
        return render(request, 'tutor_leader/tutor_leader.html', args)
    elif user.is_tech and not user.is_leader:
        # tech
        return render(request, 'tech/tech.html', args)
    elif user.is_tech and  user.is_leader:
        # tech_leader
        return render(request, 'tech_leader/tech_leader.html', args)
