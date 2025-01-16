from django.urls import path

from  .api_views import *

urlpatterns = [
    path('libros',libro_list),
    path('libro/<int:libro_id>',libro_obtener),
    path('libros/busqueda_simple',libro_buscar),
    path('libros/busqueda_avanzada',libro_buscar_avanzado),
    path('libros/crear',libro_create),
    path('libros/editar/<int:libro_id>',libro_editar),
    path('libros/actualizar/nombre/<int:libro_id>',libro_actualizar_nombre),
    path('libros/eliminar/<int:libro_id>',libro_eliminar),
    path('clientes',cliente_list),
    path('bibliotecas',biblioteca_list),
    path('categorias',categoria_list),
    path('autores',autor_list),
    path('registrar/usuario',registrar_usuario.as_view()),
    path('usuario/token/<str:token>',obtener_usuario_token)
]