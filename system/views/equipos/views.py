from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from system.models import *
from system.forms.equipo.forms import *
from django.urls import reverse_lazy
from django.http import JsonResponse
from system.mixin import *
from django.contrib.auth.mixins import LoginRequiredMixin

class EquipoListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Equipo
    template_name = 'equipo/list.html'
    permission_required = 'view_equipo'
    #create_url = 'servicios/create.html'
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Equipo'
        context['create_url'] = reverse_lazy('equipo_create')
        return context

class EquipoCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Equipo
    form_class = EquipoForm 
    template_name = 'equipo/create.html' 
    success_url = reverse_lazy('equipo_list')
    permission_required = 'add_equipo'
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
        context['title'] = 'Registrar nuevo integrante del equipo'
        context['entity'] = 'Equipo'
        context ['icon'] = 'fas fa-plus'
        context['list_url'] = reverse_lazy('equipo_list')
        context['action'] = 'add'

        return context
    
class EquipoUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Equipo
    form_class = EquipoForm 
    template_name = 'equipo/create.html' 
    success_url = reverse_lazy('equipo_list')
    permission_required = 'change_equipo'
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
        context['title'] = 'Edición de integrante de equipo'
        context['entity'] = 'Equipo'
        context ['icon'] = 'fas fa-pencil-alt'
        context['list_url'] = reverse_lazy('equipo_list')
        context['action'] = 'edit'
        context['image_url'] = self.object.imagen.url if self.object.imagen else None

        return context

class EquipoDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = Equipo
    template_name = 'equipo/delete.html'
    success_url = reverse_lazy('equipo_list')
    permission_required = 'delete_equipo'
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
        context['title'] = 'Eliminación de integrante de equipo'
        context['entity'] = 'Equipo'
        context['list_url'] = reverse_lazy('equipo_list')
        return context