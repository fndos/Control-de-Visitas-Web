from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import jefe_required
from ..forms import BaseAnswerInlineFormSet, RequerimientoForm, JefeSignUpForm
from ..models import Answer, Requerimiento, Visita, User


class JefeSignUpView(CreateView):
    model = User
    form_class = JefeSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'jefe'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('jefes:visita_change_list')


@method_decorator([login_required, jefe_required], name='dispatch')
class VisitaListView(ListView):
    model = Visita
    ordering = ('name', )
    context_object_name = 'visitas'
    template_name = 'planificacionVisitas/jefes/visita_change_list.html'

    def get_queryset(self):
        queryset = self.request.user.visitas \
            .select_related('subject') \
            .annotate(requerimiento_count=Count('requerimientos', distinct=True)) \
            .annotate(taken_count=Count('taken_visitas', distinct=True))
        return queryset


@method_decorator([login_required, jefe_required], name='dispatch')
class VisitaCreateView(CreateView):
    model = Visita
    fields = ('name', 'subject', )
    template_name = 'planificacionVisitas/jefes/visita_add_form.html'

    def form_valid(self, form):
        visita = form.save(commit=False)
        visita.owner = self.request.user
        visita.save()
        messages.success(self.request, 'The visita was created with success! Go ahead and add some requerimientos now.')
        return redirect('jefes:visita_change', visita.pk)


@method_decorator([login_required, jefe_required], name='dispatch')
class VisitaUpdateView(UpdateView):
    model = Visita
    fields = ('name', 'subject', )
    context_object_name = 'visita'
    template_name = 'planificacionVisitas/jefes/visita_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['requerimientos'] = self.get_object().requerimientos.annotate(answers_count=Count('answers'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing visitas that belongs
        to the logged in user.
        '''
        return self.request.user.visitas.all()

    def get_success_url(self):
        return reverse('jefes:visita_change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, jefe_required], name='dispatch')
class VisitaDeleteView(DeleteView):
    model = Visita
    context_object_name = 'visita'
    template_name = 'planificacionVisitas/jefes/visita_delete_confirm.html'
    success_url = reverse_lazy('jefes:visita_change_list')

    def delete(self, request, *args, **kwargs):
        visita = self.get_object()
        messages.success(request, 'The visita %s was deleted with success!' % visita.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.visitas.all()


@method_decorator([login_required, jefe_required], name='dispatch')
class VisitaResultsView(DetailView):
    model = Visita
    context_object_name = 'visita'
    template_name = 'planificacionVisitas/jefes/visita_results.html'

    def get_context_data(self, **kwargs):
        visita = self.get_object()
        taken_visitas = visita.taken_visitas.select_related('subordinado__user').order_by('-date')
        total_taken_visitas = taken_visitas.count()
        visita_score = visita.taken_visitas.aggregate(average_score=Avg('score'))
        extra_context = {
            'taken_visitas': taken_visitas,
            'total_taken_visitas': total_taken_visitas,
            'visita_score': visita_score
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.visitas.all()


@login_required
@jefe_required
def requerimiento_add(request, pk):
    # By filtering the visita by the url keyword argument `pk` and
    # by the owner, which is the logged in user, we are protecting
    # this view at the object-level. Meaning only the owner of
    # visita will be able to add requerimientos to it.
    visita = get_object_or_404(Visita, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = RequerimientoForm(request.POST)
        if form.is_valid():
            requerimiento = form.save(commit=False)
            requerimiento.visita = visita
            requerimiento.save()
            messages.success(request, 'You may now add answers/options to the requerimiento.')
            return redirect('jefes:requerimiento_change', visita.pk, requerimiento.pk)
    else:
        form = RequerimientoForm()

    return render(request, 'planificacionVisitas/jefes/requerimiento_add_form.html', {'visita': visita, 'form': form})


@login_required
@jefe_required
def requerimiento_change(request, visita_pk, requerimiento_pk):
    # Simlar to the `requerimiento_add` view, this view is also managing
    # the permissions at object-level. By querying both `visita` and
    # `requerimiento` we are making sure only the owner of the visita can
    # change its details and also only requerimientos that belongs to this
    # specific visita can be changed via this url (in cases where the
    # user might have forged/player with the url params.
    visita = get_object_or_404(Visita, pk=visita_pk, owner=request.user)
    requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_pk, visita=visita)

    AnswerFormSet = inlineformset_factory(
        Requerimiento,  # parent model
        Answer,  # base model
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = RequerimientoForm(request.POST, instance=requerimiento)
        formset = AnswerFormSet(request.POST, instance=requerimiento)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Requerimiento and answers saved with success!')
            return redirect('jefes:visita_change', visita.pk)
    else:
        form = RequerimientoForm(instance=requerimiento)
        formset = AnswerFormSet(instance=requerimiento)

    return render(request, 'planificacionVisitas/jefes/requerimiento_change_form.html', {
        'visita': visita,
        'requerimiento': requerimiento,
        'form': form,
        'formset': formset
    })


@method_decorator([login_required, jefe_required], name='dispatch')
class RequerimientoDeleteView(DeleteView):
    model = Requerimiento
    context_object_name = 'requerimiento'
    template_name = 'planificacionVisitas/jefes/requerimiento_delete_confirm.html'
    pk_url_kwarg = 'requerimiento_pk'

    def get_context_data(self, **kwargs):
        requerimiento = self.get_object()
        kwargs['visita'] = requerimiento.visita
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        requerimiento = self.get_object()
        messages.success(request, 'The requerimiento %s was deleted with success!' % requerimiento.text)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Requerimiento.objects.filter(visita__owner=self.request.user)

    def get_success_url(self):
        requerimiento = self.get_object()
        return reverse('jefes:visita_change', kwargs={'pk': requerimiento.visita_id})
