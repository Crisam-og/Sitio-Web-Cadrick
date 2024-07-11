from django.views.generic import ListView, CreateView, DeleteView, UpdateView,DetailView
from system.models import *
from system.forms.compania.forms import *
from django.urls import reverse_lazy
from django.http import JsonResponse
from system.mixin import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

class CompaniaCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Compania
    form_class = CompaniaForm
    template_name = 'compania/create.html'
    success_url = reverse_lazy('compania_update')
    permission_required = 'add_compania'
    url_redirect = success_url
     
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
        context ['title'] = 'Configuración de Compañía'
        context ['entity'] = 'Compania'
        context ['icon'] = 'fas fa-plus'
        context['notificaciones'] = Notificaciones.objects.all().count() 
        context['notificaciones_filter'] = Notificaciones.objects.all()[:3] 
        context ['list_url'] = reverse_lazy('compania_update')
        context['action'] = 'add'
        return context 

    
class CompaniaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Compania
    form_class = CompaniaForm
    template_name = 'compania/create.html'
    success_url = reverse_lazy('compania_update')
    permission_required = 'change_compania'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        # Verifica si hay alguna instancia de Compania
        if not Compania.objects.exists():
            return redirect('compania_create')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            # Obtener la única instancia de Compania
            return Compania.objects.get()
        except Compania.MultipleObjectsReturned:
            # Si hay múltiples, obtener la primera y eliminar las demás
            companias = Compania.objects.all()
            instance = companias.first()
            # Eliminar las demás instancias
            companias.exclude(pk=instance.pk).delete()
            return instance

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action', '')
            if action == 'edit':
                instance = self.get_object()
                form = self.get_form_class()(request.POST, instance=instance)
                if form.is_valid():
                    form.save()
                    data['success'] = True
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Configuración de Compañía'
        context['entity'] = 'Compania'
        context['icon'] = 'fas fa-pencil-alt'
        context['notificaciones'] = Notificaciones.objects.all().count() 
        context['notificaciones_filter'] = Notificaciones.objects.all()[:3] 
        context['list_url'] = reverse_lazy('compania_update')
        context['action'] = 'edit'
        return context
