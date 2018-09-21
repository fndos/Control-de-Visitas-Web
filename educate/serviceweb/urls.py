from django.urls import path
from . import views

app_name = 'serviceweb'

### ServiceWeb
from django.conf.urls import url, include
from tastypie.api import Api
from serviceweb.api import *

v1_api = Api(api_name='v1')

v1_api.register(UserResource())
v1_api.register(SectorResource())
v1_api.register(SchoolResource())

v1_api.register(RequirementResource())
v1_api.register(VisitResource())

#v1_api.register(ActivityResource())
v1_api.register(TechnicalFormResource())

#v1_api.register(DataApciAcademicoResource())
#v1_api.register(NoLeccionesAprobadasResource())
#v1_api.register(NoAlumnosIngresadosResource())
#v1_api.register(PromedioAcademicoResource())
#v1_api.register(NoAlumnosTrabajandoResource())
v1_api.register(PedagogicalFormResource())

v1_api.register(UserTestResource())
v1_api.register(SectorTestResource())


urlpatterns = [
    ### ServiceWeb
    url(r'^api/', include(v1_api.urls)),
]

