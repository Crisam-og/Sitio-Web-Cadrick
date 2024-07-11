from django.urls import path, include
from system.views.servicios.views import *
from system.views.publicidad.views import *
from system.views.capacitadores.views import *
from system.views.cursos.views import *
from system.views.clientes.views import *
from system.views.equipos.views import *
from system.views.proyectos.views import *
from system.views.home.views import *
from system.views.inscripciones.views import *
from system.views.compania.views import *
from system.views.publicidad.views import *
from system.views.tiposervicio.views import *

from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('home/', HomeTemplateView.as_view(), name='home'), 
    path('summernote/', include('django_summernote.urls')),
    path('servicios/list/', ServicioListView.as_view(), name='servicios_list'), 
    path('servicios/add/', ServicioCreateView.as_view(), name='servicios_create'),  
    path('servicios/edit/<uuid:pk>/', ServicioUpdateView.as_view(), name='servicios_update'),  
    path('servicios/delete/<uuid:pk>/', ServicioDeleteView.as_view(), name='servicios_delete'),  
    
    
    path('tipo-servicio/list/', TipoServicioListView.as_view(), name='tservicios_list'), 
    path('tipo-servicio/add/', TipoServicioCreateView.as_view(), name='tservicios_create'),  
    path('tipo-servicio/edit/<uuid:pk>/', TipoServicioUpdateView.as_view(), name='tservicios_update'),  
    path('tipo-servicio/delete/<uuid:pk>/', TipoServicioDeleteView.as_view(), name='tservicios_delete'), 
    
    path('capacitadores/list/', CapacitadorListView.as_view(), name='capacitador_list'), 
    path('capacitadores/add/', CapacitadorCreateView.as_view(), name='capacitador_create'),  
    path('capacitadores/edit/<uuid:pk>/', CapacitadorUpdateView.as_view(), name='capacitador_update'),  
    path('capacitadores/delete/<uuid:pk>/', CapacitadorDeleteView.as_view(), name='capacitador_delete'), 
    
    
    path('cursos/list/', CursoListView.as_view(), name='cursos_list'), 
    path('cursos/add/', CursoCreateView.as_view(), name='cursos_create'),  
    path('cursos/edit/<uuid:pk>/', CursoUpdateView.as_view(), name='cursos_update'),  
    path('cursos/delete/<uuid:pk>/', CursoDeleteView.as_view(), name='cursos_delete'), 
    path('cursos/detalle-curso/<uuid:id>/', CursoDetailView.as_view(), name='cursos_detail'),
    
    path('clientes/list/', ClienteListView.as_view(), name='clientes_list'), 
    path('clientes/add/', ClienteCreateView.as_view(), name='clientes_create'),  
    path('clientes/edit/<uuid:pk>/', ClienteUpdateView.as_view(), name='clientes_update'),  
    path('clientes/delete/<uuid:pk>/', ClienteDeleteView.as_view(), name='clientes_delete'), 
    
    
    path('equipo/list/', EquipoListView.as_view(), name='equipo_list'), 
    path('equipo/add/', EquipoCreateView.as_view(), name='equipo_create'),  
    path('equipo/edit/<uuid:pk>/', EquipoUpdateView.as_view(), name='equipo_update'),  
    path('equipo/delete/<uuid:pk>/', EquipoDeleteView.as_view(), name='equipo_delete'),
    
    path('proyectos/list/', ProyectoListView.as_view(), name='proyecto_list'), 
    path('proyectos/add/', ProyectoCreateView.as_view(), name='proyecto_create'),  
    path('proyectos/edit/<uuid:pk>/', ProyectoUpdateView.as_view(), name='proyecto_update'),  
    path('proyectos/delete/<uuid:pk>/', ProyectoDeleteView.as_view(), name='proyecto_delete'),
    
    path('inscripciones/list/', InscripcionesListView.as_view(), name='inscripciones_list'), 
    path('inscripciones/edit/<uuid:pk>/', InscripcionesUpdateView.as_view(), name='inscripciones_update'),  
    path('inscripciones/delete/<uuid:pk>/',  InscripcionesDeleteView.as_view(), name='inscripciones_delete'), 
    path('inscripciones/detalle-inscripcion/<uuid:id>/',  InscripcionDetailView.as_view(), name='inscripciones_detail'),
    path('inscripciones/count/', InscripcionesCountView.as_view(), name='inscripciones_count'),

    
    path('configuraciones/add/', CompaniaCreateView.as_view(), name='compania_create'), 
    path('configuraciones/edit/',  CompaniaUpdateView.as_view(), name='compania_update'),  
    
    path('image-and-text/add/', GaleriaCreateView.as_view(), name='galeria_create'), 
    path('image-and-text/edit/',  GaleriaUpdateView.as_view(), name='galeria_update'),  
    path('delete-image/<uuid:pk>/', ImageGaleriaDeleteView.as_view(), name='delete_image'),
    
     
    path('marcar-notificacion-leida/', marcar_notificacion_leida, name='marcar_notificacion_leida'),



 ]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)