from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from system.models import *
from system.forms.inscripciones.forms import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from django.http import JsonResponse

class NosotrosListView(ListView):
    model = Compania
    template_name = 'nosotros/about.html'

    #create_url = 'servicios/create.html'
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titleOne'] = 'Acerca de nosotros'
        context['titleTwo'] = 'Nuestra misión y visión'
        context['comp'] = Compania.objects.first()
        context['team'] = Equipo.objects.all()
        context['publicidad'] = Galeria.objects.first()

        return context