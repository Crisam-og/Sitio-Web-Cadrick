from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from system.models import *
from system.forms.tiposervicio.forms import *
from django.urls import reverse_lazy
from django.http import JsonResponse
from system.mixin import *
from django.contrib.auth.mixins import LoginRequiredMixin

class TipoServicioListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = TipoServicio
    template_name = 'tservicios/list.html'
    permission_required = 'view_tiposervicio'
    #create_url = 'servicios/create.html'
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de tipos servicios'
        context['create_url'] = reverse_lazy('tservicios_create')
        return context

class TipoServicioCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = TipoServicio
    form_class = TipoServicioForm 
    template_name = 'tservicios/create.html' 
    success_url = reverse_lazy('tservicios_list')
    permission_required = 'add_tiposervicio'
    url_redirect = success_url
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No hay registros'
            
        except Exception as e:
            data['error'] = str(e)
            
        return JsonResponse(data) 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar nuevo servicio'
        context['entity'] = 'Servicios'
        context ['icon'] = 'fas fa-plus'
        context['list_url'] = reverse_lazy('tservicios_list')
        context['action'] = 'add'

        return context
    
class TipoServicioUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = TipoServicio
    form_class = TipoServicioForm
    template_name = 'tservicios/create.html'
    success_url = reverse_lazy('tservicios_list')
    permission_required = 'change_tiposervicio'
    url_redirect = success_url
    
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    form.save() 
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No hay registros'
            
        except Exception as e:
            data['error'] = str(e)
            
        return JsonResponse(data) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición del Tipo de servicio'
        context['entity'] = 'TipoServicios'
        context ['icon'] = 'fas fa-pencil-alt'
        context['list_url'] = reverse_lazy('tservicios_list')
        context['action'] = 'edit'

        return context

class TipoServicioDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = TipoServicio
    template_name = 'tservicios/delete.html'
    success_url = reverse_lazy('tservicios_list')
    permission_required = 'delete_tiposervicio'
    url_redirect = success_url
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de Tipo Servicios'
        context['entity'] = 'TipoServicios'
        context['list_url'] = reverse_lazy('tservicios_list')
        return context