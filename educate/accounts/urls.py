from django.urls import path
#from django.contrib.auth import login
from django.contrib.auth.views import login, logout
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', login, {'template_name': 'accounts/login.html'}),
    path('logout/', logout, name='logout'),
]
