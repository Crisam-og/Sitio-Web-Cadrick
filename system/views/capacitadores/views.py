from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from system.models import *
from system.forms.capacitadores.forms import *
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from system.mixin import *
from django.contrib.auth.mixins import LoginRequiredMixin

class CapacitadorListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Capacitador
    template_name = 'capacitadores/list.html'
    permission_required = 'view_capacitador'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['title'] = 'Listado de Capacitadores'
        context['create_url'] = reverse_lazy('capacitador_create')
        return context
    
class CapacitadorCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Capacitador
    form_class = CapacitadorForm
    template_name = 'capacitadores/create.html'
    success_url = reverse_lazy('capacitador_list')
    permission_required = 'add_capacitador'
    url_redirect = success_url
    
    @method_decorator(login_required)
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
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
            
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['title'] = 'Registrar nuevo capacitador'
        context ['entity'] = 'Capacitador'
        context ['icon'] = 'fas fa-plus'
        context ['list_url'] = reverse_lazy('capacitador_list')
        context['action'] = 'add'
        return context
    
class CapacitadorUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Capacitador
    form_class = CapacitadorForm
    template_name = 'capacitadores/create.html'
    success_url = reverse_lazy('capacitador_list')
    permission_required = 'change_capacitador'
    url_redirect = success_url
    
    @method_decorator(login_required)
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
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
            
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['title'] = 'Editar datos del capacitador'
        context ['entity'] = 'Capacitador'
        context ['icon'] = 'fas fa-pencil-alt'
        context['list_url'] = reverse_lazy('capacitador_list')
        context['action'] = 'edit'
        context['image_url'] = self.object.imagen.url if self.object.imagen else None

        return context
    
class CapacitadorDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = Capacitador
    template_name = 'capacitadores/delete.html'
    success_url = reverse_lazy('capacitador_list')
    permission_required = 'delete_capacitador'
    url_redirect = success_url
    @method_decorator(login_required)
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
        context ['title'] = 'Eliminar capacitador'
        context ['entity'] = 'Capacitador'
        context['list_url'] = reverse_lazy('capacitador_list')
        return context
        