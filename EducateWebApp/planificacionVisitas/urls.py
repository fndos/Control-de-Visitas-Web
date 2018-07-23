from django.urls import include, path

from .views import planificacionVisitas, subordinados, jefes

urlpatterns = [
    path('', planificacionVisitas.home, name='home'),

    path('subordinados/', include(([
        path('', subordinados.VisitaListView.as_view(), name='visita_list'),
        path('perfiles/', subordinados.PerfilesSubordinadoView.as_view(), name='perfiles_subordinado'),
        path('taken/', subordinados.VisitaRealizadaListView.as_view(), name='visita_realizada_list'),
        path('visita/<int:pk>/', subordinados.realizar_visita, name='realizar_visita'),
    ], 'planificacionVisitas'), namespace='subordinados')),

    path('jefes/', include(([
        path('', jefes.VisitaListView.as_view(), name='visita_change_list'),
        path('visita/add/', jefes.VisitaCreateView.as_view(), name='visita_add'),
        path('visita/<int:pk>/', jefes.VisitaUpdateView.as_view(), name='visita_change'),
        path('visita/<int:pk>/delete/', jefes.VisitaDeleteView.as_view(), name='visita_delete'),
        path('visita/<int:pk>/results/', jefes.VisitaResultsView.as_view(), name='visita_results'),
        path('visita/<int:pk>/requerimiento/add/', jefes.requerimiento_add, name='requerimiento_add'),
        path('visita/<int:visita_pk>/requerimiento/<int:requerimiento_pk>/', jefes.requerimiento_change, name='requerimiento_change'),
        path('visita/<int:visita_pk>/requerimiento/<int:requerimiento_pk>/delete/', jefes.RequerimientoDeleteView.as_view(), name='requerimiento_delete'),
    ], 'planificacionVisitas'), namespace='jefes')),
]
