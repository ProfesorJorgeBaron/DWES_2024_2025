from django.urls import path,re_path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    
    path('libro/create/',views.libro_create,name='libro_create'),
    
    path('libro/<int:libro_id>/',views.libro_mostrar,name='libro_mostrar'),
    
    path('libros/listar',views.libros_lista,name='libro_lista'),
    
    path('libro/buscar/',views.libro_buscar,name='libro_buscar'),
    
    path('libro/buscar_avanzado/',views.libro_buscar_avanzado,name='libro_buscar_avanzado'),
    
    path('libro/editar/<int:libro_id>',views.libro_editar,name='libro_editar'),
    
    path('libro/eliminar/<int:libro_id>',views.libro_eliminar,name='libro_eliminar'),
    
]