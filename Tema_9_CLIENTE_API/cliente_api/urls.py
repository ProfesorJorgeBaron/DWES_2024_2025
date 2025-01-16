from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    
    path('libros/listar',views.libros_lista,name='libro_lista'),
    path('libro/<int:libro_id>',views.libro_obtener,name='libro_mostrar'),
    path('libro/editar/<int:libro_id>',views.libro_editar,name='libro_editar'),
    path('libro/editar/nombre/<int:libro_id>',views.libro_editar_nombre,name='libro_editar_nombre'),
    path('libro/eliminar/<int:libro_id>',views.libro_eliminar,name='libro_eliminar'),
    path('libros/busqueda_simple',views.libro_busqueda_simple,name='libro_buscar_simple'),
    path('libros/busqueda_avanzada',views.libro_busqueda_avanzada,name='libro_buscar_avanzado'),
    path('libros/crear',views.libro_crear,name='libro_crear'),
    path('registrar',views.registrar_usuario,name='registrar_usuario'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
]