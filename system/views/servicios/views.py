from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from system.models import *
from system.forms.servicios.forms import *
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse, JsonResponse
from system.mixin import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class ServicioListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Servicios
    template_name = 'servicios/list.html'
    permission_required = 'view_servicios'
    #create_url = 'servicios/create.html'
    context_object_name = 'servicios'
        
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    # def get(self, request, *args, **kwargs):
    #     services = Servicios(request.GET.get('id'))
    #     serviceimg = ImagenServicios(request.GET('servicios'))
    #     if 
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de servicios'
        context['create_url'] = reverse_lazy('servicios_create')
        return context

class ServicioCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Servicios
    form_class = ServiciosForm 
    template_name = 'servicios/create.html' 
    success_url = reverse_lazy('servicios_list')
    permission_required = 'add_servicios'
    url_redirect = success_url
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                mltpe_image = ImagenServiciosForm(request.POST, request.FILES)
                if form.is_valid() and mltpe_image.is_valid():
                    servicio_instance = form.save()
                    for imagen in request.FILES.getlist('imagen'):
                        ImagenServicios.objects.create(servicios=servicio_instance, imagen=imagen)
                else:
                    errors = []
                    for error in form.errors.values():
                        errors.extend(error)
                    for error in mltpe_image.errors.values():
                        errors.extend(error)
                    data['error'] = errors
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
        context['mimage'] = ImagenServiciosForm()
        context['list_url'] = reverse_lazy('servicios_list')
        context['action'] = 'add'
        return context
    
class ServicioUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Servicios
    form_class = ServiciosForm
    template_name = 'servicios/create.html'
    success_url = reverse_lazy('servicios_list')
    permission_required = 'change_servicios'
    url_redirect = success_url
    
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                instance = self.get_object()
                form = self.get_form_class()(request.POST, request.FILES, instance=instance)
                mltpe_image = ImagenServiciosForm(request.POST, request.FILES)
                if form.is_valid() and mltpe_image.is_valid():       
                   servicio_instance = form.save() 
                   # Handle deletion of existing images
                #    messages.success(request,"Actualizado Correctamente")
                   
                   for image in ImagenServicios.objects.filter(servicios=servicio_instance):
                        if request.POST.get(f'delete_image_{image.id}'):
                            image.delete()

                    # Handle uploading new images
                   for imagen in request.FILES.getlist('imagen'):
                        ImagenServicios.objects.create(servicios=servicio_instance, imagen=imagen)
                else:
                    errors = []
                    for error in form.errors.values():
                        errors.extend(error)
                    for error in mltpe_image.errors.values():
                        errors.extend(error)
                    data['error'] = errors
            else:
                data['error'] = 'No hay registros'
            
        except Exception as e:
            data['error'] = str(e)
            
        return JsonResponse(data) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición del servicio'
        context['entity'] = 'Servicios'
        context ['icon'] = 'fas fa-pencil-alt'
        context['list_url'] = reverse_lazy('servicios_list')
        context['mimage'] = ImagenServiciosForm()
        galeria = self.get_object()
        context['existing_images'] = galeria.imagenes.all()
        context['mivi_images'] = Galeria.objects.all()
        context['action'] = 'edit'
        

        return context

class ServicioDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = Servicios
    template_name = 'servicios/delete.html'
    success_url = reverse_lazy('servicios_list')
    permission_required = 'delete_servicios'
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
        context['title'] = 'Eliminación de Servicios'
        context['entity'] = 'Servicios'
        context['list_url'] = reverse_lazy('servicios_list')
        return context