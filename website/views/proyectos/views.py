from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from system.models import *
from django.urls import reverse_lazy

class ProyectoDetailView(DetailView):
    model = Proyectos
    template_name = 'proyectos/proyecto-details.html'
    context_object_name = 'proyecto'
    slug_field = 'id'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        # Obtiene el ID del curso desde los parámetros de la URL
        proyecto_id = self.kwargs.get('id')
        # Recupera el objeto Cursos o devuelve un 404 si no se encuentra
        return get_object_or_404(Proyectos, id=proyecto_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comp'] = Compania.objects.first()
        galeria = self.get_object()
        context['existing_images'] = galeria.imagenes.all()
        return context