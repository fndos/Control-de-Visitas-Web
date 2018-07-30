from django.urls import path
#from django.contrib.auth import login
from django.contrib.auth.views import login, logout
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.LoginRedirect, name='login_redirect'),
    path('login/', login, {'template_name': 'accounts/login.html'}, name='login'),
    path('logout/', logout, name='logout'),
    # Users
    path('users/create', views.UserCreate.as_view(), name='user_create'),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', views.UserDelete.as_view(), name='user_delete'),
    path('users/show/<int:pk>/', views.UserShow.as_view(), name='user_show'),
    # Schools
    path('schools/', views.SchoolList.as_view(), name='school_list'),
    path('schools/create', views.SchoolCreate.as_view(), name='school_create'),
    path('schools/update/<int:pk>/', views.SchoolUpdate.as_view(), name='school_update'),
    path('schools/delete/<int:pk>/', views.SchoolDelete.as_view(), name='school_delete'),
    path('schools/show/<int:pk>/', views.SchoolShow.as_view(), name='school_show'),
]
