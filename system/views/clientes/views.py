from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from system.models import *
from system.forms.clientes.forms import *
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from system.mixin import *
from django.contrib.auth.mixins import LoginRequiredMixin

class ClienteListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Clientes
    template_name = 'clientes/list.html'
    permission_required = 'view_clientes'
    #create_url = 'servicios/create.html'
    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Clientes'
        context['create_url'] = reverse_lazy('clientes_create')
        return context

class ClienteCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Clientes
    form_class = ClientesForm 
    template_name = 'clientes/create.html' 
    success_url = reverse_lazy('clientes_list')
    permission_required = 'add_clientes'
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
        context['title'] = 'Registrar nuevo Cliente'
        context['entity'] = 'Cliente'
        context ['icon'] = 'fas fa-plus'
        context['list_url'] = reverse_lazy('clientes_list')
        context['action'] = 'add'

        return context
    
class ClienteUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Clientes
    form_class = ClientesForm 
    template_name = 'clientes/create.html' 
    success_url = reverse_lazy('clientes_list')
    permission_required = 'change_clientes'
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
        context['title'] = 'Edición de Cliente'
        context['entity'] = 'Clientes'
        context ['icon'] = 'fas fa-pencil-alt'
        context['list_url'] = reverse_lazy('clientes_list')
        context['action'] = 'edit'
        context['image_url'] = self.object.imagen.url if self.object.imagen else None

        return context

class ClienteDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = Clientes
    template_name = 'clientes/delete.html'
    success_url = reverse_lazy('clientes_list')
    permission_required = 'delete_clientes'
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
        context['title'] = 'Eliminación de Clientes'
        context['entity'] = 'Clientes'
        context['list_url'] = reverse_lazy('clientes_list')
        return context