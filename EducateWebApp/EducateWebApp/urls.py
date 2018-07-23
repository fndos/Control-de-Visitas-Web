from django.urls import include, path

from planificacionVisitas.views import planificacionVisitas, subordinados, jefes

urlpatterns = [
    path('', include('planificacionVisitas.urls')),
    path('cuentas/', include('django.contrib.auth.urls')),
    path('cuentas/signup/', planificacionVisitas.SignUpView.as_view(), name='signup'),
    path('cuentas/signup/subordinado/', subordinados.SubordinadoSignUpView.as_view(), name='subordinado_signup'),
    path('cuentas/signup/jefe/', jefes.JefeSignUpView.as_view(), name='jefe_signup'),
]
