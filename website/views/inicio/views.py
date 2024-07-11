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

class IndexTemplateView(TemplateView):
    template_name = 'index/principal.html'
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titleProyectos'] = 'Proyectos'
        context['titleServi'] = 'Servicios'
        context['titleClients'] = 'Clientes'
        context['titleCursos'] = 'Cursos'
        context['proyec'] = Proyectos.objects.all()
        context['team'] = Equipo.objects.all()
        context['courses'] = Cursos.objects.filter(estado=True).order_by('fecha_de_inicio')[:3] 
        context['service'] = Servicios.objects.filter(estado=True)[:6] 
        context['publicidad'] = Galeria.objects.first()
        context['pi'] = ImagenGaleria.objects.all()
        # galeria = self.get_object()
        # context['existing_images'] = galeria.imagenes.all()
        context['client'] = Clientes.objects.all()
        context['comp'] = Compania.objects.first()
        return context