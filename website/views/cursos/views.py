from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView, UpdateView,DetailView
from system.models import *
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

class CursoListView(ListView):
    model = Cursos
    template_name = 'cursos/cursos.html'
    context_object_name = 'courses'
    paginate_by = 3
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        # Ordenar el queryset por un campo específico, por ejemplo, 'fechaDeInicio'
        return Cursos.objects.all().order_by('fecha_de_inicio')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Cursos.objects.all()
        context['comp'] = Compania.objects.first()
        return context
    
class CursoDetailView(DetailView):
    model = Cursos
    template_name = 'cursos/curso-details.html'
    context_object_name = 'curso'
    slug_field = 'id'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        # Obtiene el ID del curso desde los parámetros de la URL
        curso_id = self.kwargs.get('id')
        # Recupera el objeto Cursos o devuelve un 404 si no se encuentra
        return get_object_or_404(Cursos, id=curso_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cursos'] = Cursos.objects.exclude(id=self.object.id)
        context['comp'] = Compania.objects.first()
        return context