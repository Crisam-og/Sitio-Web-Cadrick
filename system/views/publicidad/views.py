from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from system.models import *
from system.forms.publicidad.forms import *
from system.forms.servicios.forms import *
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from system.mixin import *
from django.contrib.auth.mixins import LoginRequiredMixin


# class GaleriaListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
#     model = Galeria
#     template_name = 'publicidad/list.html'
#     permission_required = 'view_publicidad'
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Listado de publicidad'
#         context['create_url'] = reverse_lazy('publicidad_create')
#         return context

class GaleriaCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Galeria
    form_class = GaleriaForm 
    template_name = 'publicidad/create.html' 
    success_url = reverse_lazy('galeria_update')
    permission_required = 'add_galeria'
    url_redirect = success_url
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                mltpe_image = ImagenGaleriaForm(request.POST, request.FILES)
                if form.is_valid() and mltpe_image.is_valid():
                    galeria_instance = form.save()
                    for imagen in request.FILES.getlist('imagen'):
                        ImagenGaleria.objects.create(galeria=galeria_instance, imagen=imagen)
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No hay registros'
            
        except Exception as e:
            data['error'] = str(e)
            
        return JsonResponse(data) 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Textos y Imagenes'
        context['entity'] = 'Galeria'
        context ['icon'] = 'fas fa-plus'
        context['mimage'] = ImagenGaleriaForm()
        context['list_url'] = reverse_lazy('galeria_update')
        context['action'] = 'add'
        return context
    
class GaleriaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Galeria
    form_class = GaleriaForm
    template_name = 'publicidad/create.html'
    success_url = reverse_lazy('galeria_update')
    permission_required = 'change_galeria'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        if not Galeria.objects.exists():
            return redirect('galeria_create')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            return Galeria.objects.get()
        except Galeria.MultipleObjectsReturned:
            galerias = Galeria.objects.all()
            instance = galerias.first()
            galerias.exclude(pk=instance.pk).delete()
            return instance

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action', '')
            if action == 'edit':
                instance = self.get_object()
                form = self.get_form_class()(request.POST, request.FILES, instance=instance)
                mltpe_image = ImagenGaleriaForm(request.POST, request.FILES)
                if form.is_valid() and mltpe_image.is_valid():
                    galeria_instance = form.save()

                    # Handle deletion of existing images
                    for image in ImagenGaleria.objects.filter(galeria=galeria_instance):
                        if request.POST.get(f'delete_image_{image.id}'):
                            image.delete()

                    # Handle uploading new images
                    for imagen in request.FILES.getlist('imagen'):
                        ImagenGaleria.objects.create(galeria=galeria_instance, imagen=imagen)

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
        context['title'] = 'Edición de Textos y Imagenes'
        context['entity'] = 'Galeria'
        context['icon'] = 'fas fa-pencil-alt'
        context['list_url'] = reverse_lazy('galeria_update')
        context['mimage'] = ImagenGaleriaForm()
        galeria = self.get_object()
        context['existing_images'] = galeria.imagenes.all()
        context['action'] = 'edit'
        return context
    
class ImageGaleriaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = ImagenGaleria
    
    def delete(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'success': False, 'error': 'GET method not allowed'})