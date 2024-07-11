from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView, UpdateView,DetailView
from system.models import *
from system.forms.cursos.forms import *
from django.urls import reverse_lazy
from django.http import JsonResponse
from system.mixin import *
from django.contrib.auth.mixins import LoginRequiredMixin

class CursoListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Cursos
    template_name = 'cursos/list.html'
    permission_required = 'view_cursos'
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['title'] = 'Listado de Cursos'
        context['create_url'] = reverse_lazy('cursos_create')
        return context
    
class CursoCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Cursos
    form_class = CursosForm
    template_name = 'cursos/create.html'
    success_url = reverse_lazy('cursos_list')
    permission_required = 'add_cursos'
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
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
            
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['title'] = 'Registrar nuevo Curso'
        context ['entity'] = 'Cursos'
        context ['icon'] = 'fas fa-plus'
        context ['list_url'] = reverse_lazy('cursos_list')
        context['action'] = 'add'
        return context
    
class CursoUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Cursos
    form_class = CursosForm
    template_name = 'cursos/create.html'
    success_url = reverse_lazy('cursos_list')
    permission_required = 'change_cursos'
    url_redirect = success_url
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def get_initial(self):
        initial = super().get_initial()
        # Establecer la fecha de inicio inicial
        initial['fecha_de_inicio'] = self.object.fecha_de_inicio.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD
        return initial
    
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
        context ['title'] = 'Editar datos del curso'
        context ['entity'] = 'Cursos'
        context ['icon'] = 'fas fa-pencil-alt'
        context['list_url'] = reverse_lazy('cursos_list')
        context['action'] = 'edit'
        context['image_url'] = self.object.imagen.url if self.object.imagen else None

        return context
    
class CursoDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = Cursos
    template_name = 'cursos/delete.html'
    success_url = reverse_lazy('cursos_list')
    permission_required = 'delete_cursos'
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
        context ['title'] = 'Eliminar curso'
        context ['entity'] = 'Cursos'
        context['list_url'] = reverse_lazy('cursos_list')
        return context

class CursoDetailView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DetailView):
    model = Cursos
    template_name = 'cursos/curso-detail.html'
    context_object_name = 'curso'
    slug_field = 'id'
    permission_required = 'view_cursos'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        # Obtiene el ID del curso desde los parámetros de la URL
        curso_id = self.kwargs.get('id')
        # Recupera el objeto Cursos o devuelve un 404 si no se encuentra
        return get_object_or_404(Cursos, id=curso_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['title'] = 'Detalle del curso'
        curso = self.get_object()
        context['document_name'] = os.path.basename(curso.temario.name)
        return context