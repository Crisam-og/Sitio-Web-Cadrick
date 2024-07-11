from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView
from system.models import *
from system.forms import *
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone
from time import gmtime, strftime
from django.dispatch import receiver
# Importar el modelo User
from user.models import User
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST

class HomeTemplateView(LoginRequiredMixin,TemplateView):
    template_name = 'home/index.html'

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        user = request.user
        print(f"Usuario obtenido: {user}")
        group = user.get_group_session()
        print(f"Grupos obtenidos: {group}")
        return super().get(request,*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proyectos'] = Proyectos.objects.all().count()
        context['equipo'] = Equipo.objects.all().count()
        context['cursos'] = Cursos.objects.all().count()
        context['servicios'] = Servicios.objects.all().count()
        context['clientes'] = Clientes.objects.all().count()
        context['capacitadores'] = Clientes.objects.all().count()
        context['inscripciones'] = Inscripciones.objects.all().count()
        context['formatted_datetime'] = format(datetime.now().strftime("%A %d/%m/%Y %H:%M:%S"))
        context['notificaciones'] = Notificaciones.objects.all().order_by('-created_at')[:5] 
        return context

@require_POST
def marcar_notificacion_leida(request):
    notificacion_id = request.POST.get('notificacion_id')
    if notificacion_id:
        notificacion = Notificaciones.objects.get(id=notificacion_id)
        notificacion.leido = True
        notificacion.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)