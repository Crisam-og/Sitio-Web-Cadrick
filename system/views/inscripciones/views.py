from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView, View
from system.models import *
from system.forms.inscripciones.forms import *
from django.urls import reverse_lazy
from django.http import JsonResponse
from system.mixin import *
from django.contrib.auth.mixins import LoginRequiredMixin

class InscripcionesListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Inscripciones
    template_name = 'inscripciones/list.html'
    permission_required = 'view_inscripciones' 
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Inscripciones'
        return context
    def get_queryset(self):
        return Inscripciones.objects.all().order_by('-created_at')

class InscripcionesCountView(View):
    def get(self, request, *args, **kwargs):
        count = Inscripciones.objects.count()
        return JsonResponse({'count': count})
        
class InscripcionesUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Inscripciones
    form_class = IncripcionesForm
    template_name = 'inscripciones/create.html'
    success_url = reverse_lazy('inscripciones_list')
    permission_required = 'change_inscripciones'
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
        context['title'] = 'Edición de la Inscripcion'
        context['entity'] = 'Incripciones'
        context ['icon'] = 'fas fa-pencil-alt'
        context['list_url'] = reverse_lazy('inscripciones_list')
        context['action'] = 'edit'
        return context

class InscripcionesDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = Inscripciones
    template_name = 'inscripciones/delete.html'
    success_url = reverse_lazy('inscripciones_list')
    permission_required = 'delete_inscripciones'
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
        context['title'] = 'Eliminación de inscripción'
        context['entity'] = 'Incripcion'
        context['list_url'] = reverse_lazy('inscripciones_list')
        return context

class InscripcionDetailView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DetailView):
    model = Inscripciones
    template_name = 'inscripciones/inscripcion-detail.html'
    context_object_name = 'inscripcion'
    slug_field = 'id'
    permission_required = 'view_inscripciones'
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        # Obtiene el ID del curso desde los parámetros de la URL
        inscripcion_id = self.kwargs.get('id')
        # Recupera el objeto Cursos o devuelve un 404 si no se encuentra
        return get_object_or_404(Inscripciones, id=inscripcion_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['title'] = 'Datos de Inscripción'
        return context