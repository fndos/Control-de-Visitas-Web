from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from ..decorators import subordinado_required
from ..forms import SubordinadoPerfilesForm, SubordinadoSignUpForm, TakeVisitaForm
from ..models import Visita, Subordinado, TakenVisita, User


class SubordinadoSignUpView(CreateView):
    model = User
    form_class = SubordinadoSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'subordinado'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('subordinados:visita_list')


@method_decorator([login_required, subordinado_required], name='dispatch')
class PerfilesSubordinadoView(UpdateView):
    model = Subordinado
    form_class = SubordinadoPerfilesForm
    template_name = 'planificacionVisitas/subordinados/perfiles_form.html'
    success_url = reverse_lazy('subordinados:visita_list')

    def get_object(self):
        return self.request.user.subordinado

    def form_valid(self, form):
        messages.success(self.request, 'Perfiles updated with success!')
        return super().form_valid(form)


@method_decorator([login_required, subordinado_required], name='dispatch')
class VisitaListView(ListView):
    model = Visita
    ordering = ('name', )
    context_object_name = 'visitas'
    template_name = 'planificacionVisitas/subordinados/visita_list.html'

    def get_queryset(self):
        subordinado = self.request.user.subordinado
        perfiles_subordinado = subordinado.perfiles.values_list('pk', flat=True)
        taken_visitas = subordinado.visitas.values_list('pk', flat=True)
        queryset = Visita.objects.filter(subject__in=perfiles_subordinado) \
            .exclude(pk__in=taken_visitas) \
            .annotate(requerimiento_count=Count('requerimientos')) \
            .filter(requerimiento_count__gt=0)
        return queryset


@method_decorator([login_required, subordinado_required], name='dispatch')
class VisitaRealizadaListView(ListView):
    model = TakenVisita
    context_object_name = 'taken_visitas'
    template_name = 'planificacionVisitas/subordinados/visita_realizada_list.html'

    def get_queryset(self):
        queryset = self.request.user.subordinado.taken_visitas \
            .select_related('visita', 'visita__subject') \
            .order_by('visita__name')
        return queryset


@login_required
@subordinado_required
def realizar_visita(request, pk):
    visita = get_object_or_404(Visita, pk=pk)
    subordinado = request.user.subordinado

    if subordinado.visitas.filter(pk=pk).exists():
        return render(request, 'subordinados/taken_visita.html')

    total_requerimientos = visita.requerimientos.count()
    unanswered_requerimientos = subordinado.get_unanswered_requerimientos(visita)
    total_unanswered_requerimientos = unanswered_requerimientos.count()
    progress = 100 - round(((total_unanswered_requerimientos - 1) / total_requerimientos) * 100)
    requerimiento = unanswered_requerimientos.first()

    if request.method == 'POST':
        form = TakeVisitaForm(requerimiento=requerimiento, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                subordinado_answer = form.save(commit=False)
                subordinado_answer.subordinado = subordinado
                subordinado_answer.save()
                if subordinado.get_unanswered_requerimientos(visita).exists():
                    return redirect('subordinados:realizar_visita', pk)
                else:
                    correct_answers = subordinado.visita_answers.filter(answer__requerimiento__visita=visita, answer__is_correct=True).count()
                    score = round((correct_answers / total_requerimientos) * 100.0, 2)
                    TakenVisita.objects.create(subordinado=subordinado, visita=visita, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the visita %s was %s.' % (visita.name, score))
                    else:
                        messages.success(request, 'Congratulations! You completed the visita %s with success! You scored %s points.' % (visita.name, score))
                    return redirect('subordinados:visita_list')
    else:
        form = TakeVisitaForm(requerimiento=requerimiento)

    return render(request, 'planificacionVisitas/subordinados/take_visita_form.html', {
        'visita': visita,
        'requerimiento': requerimiento,
        'form': form,
        'progress': progress
    })
