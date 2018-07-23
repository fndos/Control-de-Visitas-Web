from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_jefe:
            return redirect('jefes:visita_change_list')
        else:
            return redirect('subordinados:visita_list')
    return render(request, 'planificacionVisitas/home.html')
