from django.shortcuts import render,get_object_or_404
from django.views.generic import CreateView
from system.models import *
from system.forms.inscripciones.forms import *
from django.http import Http404
from django.urls import reverse_lazy
from django.http import JsonResponse

class InscripcionesCreateView(CreateView):
    model = Inscripciones
    form_class = IncripcionesForm
    template_name = 'inscripciones/form.html'
    success_url = reverse_lazy('curso-list')
    
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
        context ['success'] = reverse_lazy('curso-list')
        context['comp'] = Compania.objects.first()
        context['action'] = 'add'
        
        return context
