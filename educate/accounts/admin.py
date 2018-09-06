from django.contrib import admin

from accounts.models import *

admin.site.register(User)
admin.site.register(Sector)
admin.site.register(School)
admin.site.register(Requirement)
admin.site.register(Visit)
admin.site.register(TechnicalForm)
admin.site.register(PedagogicalForm)
