from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from system.models import *
from django.urls import reverse_lazy

class ServiciosListView(ListView):
    model = Servicios
    template_name = 'servicios/services.html'
    context_object_name = 'services'
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        catid = self.request.GET.get('categories')
        print(f"Filtrando por categoría ID: {catid}")
        if catid:
            queryset = Servicios.objects.filter(servicio_id=catid)
        print(queryset)# Ajusta el filtro según tu modelo y campo
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['services'] = Servicios.objects.filter(estado=True)
        context['tservices'] = TipoServicio.objects.all()
        context['active_filter'] = self.request.GET.get('categories', 'all')
        context['comp'] = Compania.objects.first()
        return context
    
class ServiciosDetailView(DetailView):
    model = Servicios
    template_name = 'servicios/service-details.html'
    context_object_name = 'service'
    slug_field = 'id'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        # Obtiene el ID del curso desde los parámetros de la URL
        servicio_id = self.kwargs.get('id')
        # Recupera el objeto Cursos o devuelve un 404 si no se encuentra
        return get_object_or_404(Servicios, id=servicio_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Servicios.objects.all()
        context['tservices'] = TipoServicio.objects.all()
        current_service = self.get_object()
        context['service'] = current_service
        context['related_services'] = Servicios.objects.filter(servicio_id=current_service.servicio_id, estado=True).exclude(id=current_service.id) 
        context['comp'] = Compania.objects.first()
        galeria = self.get_object()
        context['existing_images'] = galeria.imagenes.all()
        return context