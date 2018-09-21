### ServiceWeb
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.serializers import Serializer

############
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpResponse
from django.conf.urls import url
from tastypie.utils import trailing_slash
#from django.contrib.auth.hashers import make_password, HASHERS

### Models
from accounts.models import *


class SectorTestResource(ModelResource):
    """ Modelador Tabla """
    class Meta:
        queryset = Sector.objects.all()
        resource_name = 'sectortest'
        fields = ['id','name','description']
        #allowed_methods = ['get','post','put']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        filtering = {
            'name': ALL,
        }
        include_resource_uri = False
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        serializer = Serializer(formats=['json',])
        ordering = ['id']

    """Deserialize for multipart Data"""
    def deserialize(self, request, data, format=None):
        if format is None:
            format = request.META.get('CONTENT_TYPE','application/json')
        if format == 'application/x-www-form-urlencoded':
            return request.POST
        elif format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data
        return super(SectorTestResource, self).deserialize(request, data, format)

    """ Create """
    #def obj_create(self, bundle, **kwargs):
    #    return super(SectorTestResource, self).obj_create(bundle, user=bundle.request.user)

    """ Update """
    def obj_update(self, bundle, **kwargs):
        return super(SectorTestResource, self).obj_update(bundle, **kwargs)


class UserTestResource(ModelResource):
    """ Modelador Tabla """
    class Meta:
        queryset = User.objects.all()
        resource_name = 'usuariotest'
        fields = ['id','dni','username','password','user_type','first_name','last_name','phone_number']
        allowed_methods = ['get','post']
        include_resource_uri = False
        #authentication = ApiKeyAuthentication()
        authorization = Authorization()

    """Deserialize for multipart Data"""
    def deserialize(self, request, data, format=None):
        if format is None:
            format = request.META.get('CONTENT_TYPE','application/json')
        if format == 'application/x-www-form-urlencoded':
            return request.POST
        elif format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data
        return super(UserTestResource, self).deserialize(request, data, format)

    """ Include login in URL """
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    """ Function Login """
    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'text/html'))
        us = data.get('us', '')
        ps = data.get('ps', '')
        user = authenticate(username=us, password=ps)
        if user:
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True,
                    'uid': user.id
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                    }, HttpForbidden )
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
                }, HttpUnauthorized )

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, { 'success': True })
        else:
            return self.create_response(request, { 'success': False }, HttpUnauthorized)


class SectorResource(ModelResource):
    """ Modelador Tabla """
    class Meta:
        queryset = Sector.objects.all()
        resource_name = 'sector'
        #fields = ['id','name','description']
        allowed_methods = ['get','post','put']
        filtering = {
            'name': ALL,
        }
        include_resource_uri = False
        #authentication = ApiKeyAuthentication()
        #authorization = Authorization()
        serializer = Serializer(formats=['json',])
        ordering = ['id']


class UserResource(ModelResource):
    """ Modelador User """
    class Meta:
        queryset = User.objects.all()
        resource_name = 'usuario'
        #fields = ['id','dni','username','password','user_type','first_name','last_name','phone_number']
        allowed_methods = ['get','post']
        filtering = {
            'username': ('exact',),
        }
        include_resource_uri = False
        #authentication = ApiKeyAuthentication()
        authorization = Authorization()
        serializer = Serializer(formats=['json',])
        ordering = ['id']

    """ Deserialize for Content-type """
    def deserialize(self, request, data, format=None):
        if format is None:
            format = request.META.get('CONTENT_TYPE','application/json')
        if format == 'application/x-www-form-urlencoded':
            return request.POST
        elif format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data
        return super(UserResource, self).deserialize(request, data, format)

    """ Include login in URL """
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('login'), name="api_login"),
        ]

    """ Function Login """
    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        _user = data.get('us', '')
        _pass = data.get('ps', '')
        user = authenticate(username=_user, password=_pass)
        if user:
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True,
                    'uid': user.id
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                    }, HttpForbidden )
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
                }, HttpUnauthorized )


class SchoolResource(ModelResource):
    """ FK """
    sector = fields.ForeignKey(SectorResource, attribute='sector', null=True, full=True)

    """ Modelador School """
    class Meta:
        queryset = School.objects.all()
        resource_name = 'school'
        #fields = ['id','amie','name','phone_number','address','reference','workday','parish','priority','ambassador_in','sector']
        allowed_methods = ['get','post']
        filtering = {
            'amie': ALL,
            'name': ALL,
            'ambassador_in': ALL,
            'workday': ALL,
            'priority': ALL,
            'sector': ALL_WITH_RELATIONS,
        }
        include_resource_uri = False
        #authentication = ApiKeyAuthentication()
        #authorization = Authorization()
        serializer = Serializer(formats=['json',])
        ordering = ['id']


################################################################################
### ANDROID
################################################################################

class RequirementResource(ModelResource):
    """ FK """
    school = fields.ForeignKey(SchoolResource, attribute='school', null=True, full=True)
    user = fields.ForeignKey(UserResource, attribute='user', null=True, full=True)

    """ Modelador Tabla """
    class Meta:
        queryset = Requirement.objects.all()
        resource_name = 'requirement'
        #fields = ['id','reason','type','state','school','user']
        #allowed_methods = ['get','post']
        list_allowed_methods = ['get', 'post','put','patch']
        detail_allowed_methods = ['get', 'post', 'put','patch']
        filtering = {
        #    'id': ALL,
            'reason': ALL,
            'type': ALL,
            'state': ALL,
            'school': ALL_WITH_RELATIONS,
            'user': ALL_WITH_RELATIONS,
        }
        include_resource_uri = False
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        serializer = Serializer(formats=['json',])
        ordering = ['id']

    """ Deserialize for Content-type"""
    def deserialize(self, request, data, format=None):
        if format is None:
            format = request.META.get('CONTENT_TYPE','application/json')
        if format == 'application/x-www-form-urlencoded':
            return request.POST
        elif format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data
        return super(RequirementResource, self).deserialize(request, data, format)

    """ Update """
    def obj_update(self, bundle, **kwargs):
        return super(RequirementResource, self).obj_update(bundle, **kwargs)


class VisitResource(ModelResource):
    """ FK """
    requirement = fields.ForeignKey(RequirementResource, attribute='requirement', null=True, full=True)
    user = fields.ForeignKey(UserResource, attribute='user', null=True, full=True)

    """ Modelador Tabla """
    class Meta:
        queryset = Visit.objects.all()
        resource_name = 'visit'
        #fields = ['id','date_planned','check_in','check_out','coordinates_lat_in','coordinates_lon_in','coordinates_lat_out','coordinates_lon_out','type','observation','requirement','user']
        #allowed_methods = ['get','post']
        list_allowed_methods = ['get', 'post','put','patch']
        detail_allowed_methods = ['get', 'post', 'put','patch']
        filtering = {
        #    'id': ALL,
            'date_planned': ALL,
            'requirement': ALL_WITH_RELATIONS,
            'user': ALL_WITH_RELATIONS,
        }
        include_resource_uri = False
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        serializer = Serializer(formats=['json',])
        ordering = ['id']

    """ Deserialize for Content-type """
    def deserialize(self, request, data, format=None):
        if format is None:
            format = request.META.get('CONTENT_TYPE','application/json')
        if format == 'application/x-www-form-urlencoded':
            return request.POST
        elif format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data
        return super(VisitResource, self).deserialize(request, data, format)

    """ Update """
    def obj_update(self, bundle, **kwargs):
        return super(VisitResource, self).obj_update(bundle, **kwargs)


class TechnicalFormResource(ModelResource):
    """ FK """
    visit = fields.ForeignKey(VisitResource, attribute='visit', null=True, full=True)

    """ Modelador Tabla """
    class Meta:
        queryset = TechnicalForm.objects.all()
        resource_name = 'technicalform'
        #fields = ['id','visit','action_taken','observation','activity']
        #allowed_methods = ['get','post']
        list_allowed_methods = ['get', 'post','put']
        detail_allowed_methods = ['get', 'post', 'put']
        filtering = {
            'visit': ALL_WITH_RELATIONS,
        }
        include_resource_uri = False
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        serializer = Serializer(formats=['json',])
        ordering = ['id']

    """ Deserialize for Content-type """
    def deserialize(self, request, data, format=None):
        if format is None:
            format = request.META.get('CONTENT_TYPE','application/json')
        if format == 'application/x-www-form-urlencoded':
            return request.POST
        elif format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data
        return super(TechnicalFormResource, self).deserialize(request, data, format)

    """ Update """
    def obj_update(self, bundle, **kwargs):
        return super(TechnicalFormResource, self).obj_update(bundle, **kwargs)


class PedagogicalFormResource(ModelResource):
    """ FK """
    visit = fields.ForeignKey(VisitResource, attribute='visit', null=True, full=True)

    """ Modelador Tabla """
    class Meta:
        queryset = PedagogicalForm.objects.all()
        resource_name = 'pedagogicalform'
        #fields = ['id','visit_number','extracurricular','internet','action_taken','visit','data_apci_academico']
        #allowed_methods = ['get','post']
        list_allowed_methods = ['get', 'post','put']
        detail_allowed_methods = ['get', 'post', 'put']
        filtering = {
            'visit': ALL_WITH_RELATIONS,
            'data_apci_academico': ALL_WITH_RELATIONS,
        }
        include_resource_uri = False
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        serializer = Serializer(formats=['json',])
        ordering = ['id']

    """ Deserialize for Content-type"""
    def deserialize(self, request, data, format=None):
        if format is None:
            format = request.META.get('CONTENT_TYPE','application/json')
        if format == 'application/x-www-form-urlencoded':
            return request.POST
        elif format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data
        return super(PedagogicalFormResource, self).deserialize(request, data, format)

    """ Update """
    def obj_update(self, bundle, **kwargs):
        return super(PedagogicalFormResource, self).obj_update(bundle, **kwargs)






