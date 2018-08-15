from django.urls import path
#from django.contrib.auth import login
from django.contrib.auth.views import login, logout
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.LoginRedirect, name='login_redirect'),
    path('login/', login, {'template_name': 'accounts/login.html'}, name='login'),
    path('logout/', logout, name='logout'),
    ############################# TECH_LEADER (t) ##############################
    # Users
    path('t/users/create', views.UserCreate.as_view(), name='user_create'),
    path('t/users/', views.UserList.as_view(), name='user_list'),
    path('t/users/update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    path('t/users/delete/<int:pk>/', views.UserDelete.as_view(), name='user_delete'),
    path('t/users/show/<int:pk>/', views.UserShow.as_view(), name='user_show'),
    # Schools
    path('t/schools/', views.SchoolList.as_view(), name='school_list'),
    path('t/schools/create', views.SchoolCreate.as_view(), name='school_create'),
    path('t/schools/update/<int:pk>/', views.SchoolUpdate.as_view(), name='school_update'),
    path('t/schools/delete/<int:pk>/', views.SchoolDelete.as_view(), name='school_delete'),
    path('t/schools/show/<int:pk>/', views.SchoolShow.as_view(), name='school_show'),
    # Visit
    path('t/visits/', views.VisitList.as_view(), name='visit_list'),
    path('t/visits/create', views.VisitCreate.as_view(), name='visit_create'),
    path('t/visits/update/<int:pk>/', views.VisitUpdate.as_view(), name='visit_update'),
    path('t/visits/delete/<int:pk>/', views.VisitDelete.as_view(), name='visit_delete'),
    path('t/visits/show/<int:pk>/', views.VisitShow.as_view(), name='visit_show'),
    # Requeriment
    path('t/requirements/', views.RequirementList.as_view(), name='requirement_list'),
    path('t/requirements/create', views.RequirementCreate.as_view(), name='requirement_create'),
    path('t/requirements/update/<int:pk>/', views.RequirementUpdate.as_view(), name='requirement_update'),
    path('t/requirements/delete/<int:pk>/', views.RequirementDelete.as_view(), name='requirement_delete'),
    path('t/requirements/show/<int:pk>/', views.RequirementShow.as_view(), name='requirement_show'),
    ############################# TUTOR_LEADER (r) #############################
    ############################# TUTOR (nr) ###################################
    ############################# TECH (nt) ####################################
]
