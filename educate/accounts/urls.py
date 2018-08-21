from django.urls import path
#from django.contrib.auth import login
from django.contrib.auth.views import login, logout
from .views.tech_leader import views
from .views.tutor_leader import views as tutor_leader
from .views.tech import views as tech

app_name = 'accounts'

urlpatterns = [
    ############################# LOGIN REDIRECT ###############################
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
    # Sector
    path('t/sectors/create', views.SectorCreate.as_view(), name='sector_create'),
    path('t/sectors/', views.SectorList.as_view(), name='sector_list'),
    path('t/sectors/update/<int:pk>/', views.SectorUpdate.as_view(), name='sector_update'),
    path('t/sectors/delete/<int:pk>/', views.SectorDelete.as_view(), name='sector_delete'),
    path('t/sectors/show/<int:pk>/', views.SectorShow.as_view(), name='sector_show'),
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
    # Planning
    path('r/planning/', tutor_leader.PlanningList.as_view(), name='planning_list'),
    path('r/planning/create/requirement', tutor_leader.RequirementCreate.as_view(), name='planning_requirement_create'),
    path('r/planning/create/visit', tutor_leader.VisitCreate.as_view(), name='planning_visit_create'),
    path('r/planning/show/<int:pk>/', tutor_leader.VisitShow.as_view(), name='planning_show'),
    path('r/planning/update/requirement/<int:pk>/', tutor_leader.RequirementUpdate.as_view(), name='planning_requirement_update'),
    path('r/planning/update/visit/<int:pk>/', tutor_leader.VisitUpdate.as_view(), name='planning_visit_update'),
    path('r/planning/delete/<int:pk>/', tutor_leader.VisitDelete.as_view(), name='planning_delete'),
    # Visit
    path('r/visits/', tutor_leader.VisitList.as_view(), name='visit_list_tutor_leader'),
    path('r/visits/show/<int:pk>/', tutor_leader.VisitDetail.as_view(), name='visit_show_tutor_leader'),
    # Requeriment
    path('r/requirements/', tutor_leader.RequirementList.as_view(), name='requirement_list_tutor_leader'),
    path('r/requirements/show/<int:pk>/', tutor_leader.RequirementShow.as_view(), name='requirement_show_tutor_leader'),
    ############################# TUTOR (nr) ###################################

    ############################# TECH (nt) ####################################
    # Visit
    path('nt/visits/', tech.VisitList.as_view(), name='visit_list_tech'),
    path('nt/visits/show/<int:pk>/', tech.VisitShow.as_view(), name='visit_show_tech'),
]
