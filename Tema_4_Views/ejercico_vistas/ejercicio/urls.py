from django.urls import path
from .import views

urlpatterns = [
    
    path('',views.index,name='index'), 
    
    
    path('proyectos',views.listar_proyectos,name='listar_proyectos'),
    
    path('proyectos/tareas/<int:proyecto_id>/',views.listar_tareas_proyecto,name='listar_tareas_proyecto'), 
    
    path('tareas/usuarios/<int:tarea_id>/',views.listar_usuarios_tarea,name='listar_usuarios_tarea'), 
    
    path('tareas/usuario/<int:usuario_id>/<str:texto>/',views.listar_tareas_texto_usuario,name='listar_tareas_texto_usuario'), 
    
    path('tareas/<int:anyo_desde>/<int:anyo_hasta>',views.listar_tareas_anyos,name='listar_tareas_anyos'), 
    
    path('cometario/ultimo/proyecto/<int:proyecto_id>/',views.ultimo_comentario_proyecto,name='ultimo_comentario_proyecto'),
    
    path('cometarios/tarea/<int:tarea_id>/<int:anyo>/<str:texto>/',views.listar_comentarios_filtro,name='listar_comentarios_filtro'),
    
    path('etiquetas/proyecto/<int:proyecto_id>/',views.listar_etiquetas_proyecto,name='listar_etiquetas_proyecto'),
    
    path('usuarios_no_asignados/',views.usuarios_no_asignados,name='usuarios_no_asignados'),
]