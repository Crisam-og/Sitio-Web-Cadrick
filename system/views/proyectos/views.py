from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from system.models import *
from system.forms.proyectos.forms import *
from django.urls import reverse_lazy
from django.http import JsonResponse
from system.mixin import *
from django.contrib.auth.mixins import LoginRequiredMixin

class ProyectoListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Proyectos
    template_name = 'proyectos/list.html'
    permission_required = 'view_proyectos'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de proyectos'
        context['create_url'] = reverse_lazy('proyecto_create')
        return context

class ProyectoCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Proyectos
    form_class = ProyectoForm 
    template_name = 'proyectos/create.html' 
    success_url = reverse_lazy('proyecto_list')
    permission_required = 'add_proyectos'
    url_redirect = success_url
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                mltpe_image = ImagenProyectoForm(request.POST, request.FILES)
                if form.is_valid() and mltpe_image.is_valid():
                    proyecto_instance = form.save()
                    for imagen in request.FILES.getlist('imagen'):
                        ImagenProyectos.objects.create(proyecto=proyecto_instance, imagen=imagen)
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
        context['title'] = 'Registrar nuevo proyecto'
        context['entity'] = 'Proyectos'
        context ['icon'] = 'fas fa-plus'
        context['mimage'] = ImagenProyectoForm()
        context['list_url'] = reverse_lazy('proyecto_list')
        context['action'] = 'add'

        return context
    
class ProyectoUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Proyectos
    form_class = ProyectoForm
    template_name = 'proyectos/create.html'
    success_url = reverse_lazy('proyecto_list')
    permission_required = 'change_proyectos'
    url_redirect = success_url
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def get_initial(self):
        initial = super().get_initial()
        # Establecer la fecha de inicio inicial
        initial['fecha_de_proyecto'] = self.object.fecha_de_proyecto.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD
        return initial
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                instance = self.get_object()
                form = self.get_form_class()(request.POST, request.FILES, instance=instance)
                mltpe_image = ImagenProyectoForm(request.POST, request.FILES)
                if form.is_valid() and mltpe_image.is_valid():       
                   proyecto_instance = form.save() 
                   # Handle deletion of existing images
                #    messages.success(request,"Actualizado Correctamente")
                   
                   for image in ImagenProyectos.objects.filter(proyecto=proyecto_instance):
                        if request.POST.get(f'delete_image_{image.id}'):
                            image.delete()

                    # Handle uploading new images
                   for imagen in request.FILES.getlist('imagen'):
                        ImagenProyectos.objects.create(proyecto=proyecto_instance, imagen=imagen)
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
        context['title'] = 'Edición de proyectos'
        context['entity'] = 'Proyectos'
        context ['icon'] = 'fas fa-pencil-alt'
        context['list_url'] = reverse_lazy('proyecto_list')
        context['action'] = 'edit'
        context['mimage'] = ImagenProyectoForm()
        galeria = self.get_object()
        context['existing_images'] = galeria.imagenes.all()
        # context['image_url'] = self.object.imagen.url if self.object.imagen else None
        return context

class ProyectoDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = Proyectos
    template_name = 'proyectos/delete.html'
    success_url = reverse_lazy('proyecto_list')
    permission_required = 'delete_proyectos'
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
        context['title'] = 'Eliminación de Proyectos'
        context['entity'] = 'Proyectos'
        context['list_url'] = reverse_lazy('proyecto_list')
        return context