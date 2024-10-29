from django.shortcuts import render
from django.db.models import Q,Prefetch
from .models import Proyecto,Tarea,Usuario,Comentario,Etiqueta

"""
    1-Desde una página de Inicio debe poder acceder a todas las URLs que se indiquen. 
    Esto no significa que no pueda acceder a algunas URLs desde otros sitios. 
    Pero desde la página de Inicio tengo que poder acceder a un ejemplo de las 
    URLs que se realicen a continuación.    
"""
def index(request):
    return render(request, 'index.html') 


"""
    2-Crea una URL que muestre una lista de todos los proyectos de la aplicación 
    con sus datos correspondientes.
"""

def listar_proyectos(request):
    
    proyectos = (Proyecto.objects.select_related("creador")
                 .prefetch_related("colaboradores",Prefetch("proyecto_tareas"))
                ).all()
    return render(request, "proyecto/lista.html", {"proyectos":proyectos})
   
"""
    3-Crear una URL que muestre todas las tareas que están asociadas a un proyecto,
    ordenadas por fecha de creación descendente.
"""   
def listar_tareas_proyecto(request,proyecto_id):
    proyecto_mostrar = Proyecto.objects.get(id=proyecto_id)

    tareas = (Tarea.objects.select_related("creador","proyecto").
              prefetch_related("usuarios_asignados",Prefetch("etiquetas_tareas"),
                               Prefetch("comentarios_tarea"),
                               Prefetch("comentarios_tarea__autor")  
                               )
            )
    tareas = tareas.filter(proyecto=proyecto_id).order_by("-fecha_creacion").all()
    
    return render(request, "tarea/lista.html", {"tareas":tareas, "proyecto":proyecto_mostrar})
   

"""
   4- Crear una URL que muestre todos los usuarios que están asignados a una tarea ordenados 
   por la fecha de asignación de la tarea de forma ascendente. 
"""   
def listar_usuarios_tarea(request,tarea_id):
    tarea = Tarea.objects.get(id=tarea_id)
    #Version Corta
    """usuarios = (Usuario.objects
                        .filter(asignaciontarea__tarea=tarea_id)
                        .order_by("asignaciontarea__fecha_asignacion")
    ).all()"""

    #Version Larga
   
    usuarios = (Usuario.objects.prefetch_related(
                            Prefetch("creador_proyecto"),
                            Prefetch("colaboradores_proyecto"),
                            Prefetch("creador_tarea"),
                            Prefetch("colaboradores_tarea"),
                            Prefetch("comentarios_creador"),
                               )
                        .filter(asignaciontarea__tarea=tarea_id)
                        .order_by("asignaciontarea__fecha_asignacion")
    ).all()
    
    
    return render(request, "usuario/lista_completa.html", {"usuarios":usuarios,"tarea":tarea})
    

"""
    5-Crear una URL que muestre todas las tareas que tengan un texto en concreto en las observaciones 
    a la hora de asignarlas a un usuario.
"""   
def listar_tareas_texto_usuario(request,usuario_id,texto):
    usuario = Usuario.objects.get(id=usuario_id)
    tareas = (Tarea.objects.select_related("creador","proyecto").
              prefetch_related("usuarios_asignados",Prefetch("etiquetas_tareas"),
                               Prefetch("comentarios_tarea"),
                               Prefetch("comentarios_tarea__autor")  
                                )
    ).filter(asignaciontarea__observaciones__contains=texto,asignaciontarea__usuario=usuario_id).all()
 
    return render(request, "tarea/lista_filtro_usuario.html", {"tareas":tareas, "usuario": usuario})
 
"""
    6-Crear una URL que muestre todos las tareas que se han creado entre dos años 
    y el estado sea “Completada”.
"""   
def listar_tareas_anyos(request,anyo_desde,anyo_hasta):
    tareas = (Tarea.objects.select_related("creador","proyecto").
              prefetch_related("usuarios_asignados",Prefetch("etiquetas_tareas"),
                               Prefetch("comentarios_tarea"),
                               Prefetch("comentarios_tarea__autor")  
                               )
    ).filter(fecha_creacion__year__gte=anyo_desde,fecha_creacion__year__lte=anyo_hasta,estado='Co')          
    return render(request, "tarea/lista.html", {"tareas":tareas})
    
    
"""
    7-Crear una URL que obtenga el último usuario que ha comentado en una tarea de un proyecto en concreto.
"""   
def ultimo_comentario_proyecto(request,proyecto_id):
    comentario = (Comentario.objects.select_related("autor","tarea").
                   prefetch_related(Prefetch("tarea__proyecto"))
                  .filter(tarea__proyecto=proyecto_id)
                  .order_by("-fecha_comentario")[0:1].get()                        
    )
    usuario = comentario.autor
    
    
    """usuario = (Usuario.objects.filter(comentarios_creador__tarea__proyecto=proyecto_id).
                order_by("-comentarios_creador__fecha_comentario")[:1].get()
              )"""
    
    return render(request, "usuario/usuario.html", {"usuario":usuario})
    
    
"""
    8-Crear una URL que obtenga todos los comentarios de una tarea que empiecen 
    por la palabra que se pase en la URL y que el año del comentario sea uno en concreto.
"""   
def listar_comentarios_filtro(request,tarea_id,anyo,texto):
    tarea = Tarea.objects.get(id=tarea_id)
    
    comentarios = (Comentario.objects.select_related("autor")
                  .filter(tarea=tarea_id)
                  .filter(fecha_comentario__year=anyo)
                  .filter(contenido__startswith=texto)
    ).all()
    
    return render(request, "comentario/lista.html", {"tarea":tarea,"comentarios":comentarios})
    
    
"""
    9-Crear una URL que obtenga todas las etiquetas que se han 
    usado en todas las tareas de un proyecto.
"""   
def listar_etiquetas_proyecto(request,proyecto_id):
    proyecto = Proyecto.objects.get(id=proyecto_id)
    
    etiquetas = (Etiqueta.objects.prefetch_related("tarea")
                 .filter(tarea__proyecto=proyecto_id)
    ).distinct().all()
    
    return render(request, "etiqueta/lista.html", {"proyecto":proyecto,"etiquetas":etiquetas})
    

"""
    10-Crear una URL que muestre todos los usuarios que no están asignados a una tarea.
"""   
def usuarios_no_asignados(request):
    usuarios = (Usuario.objects.prefetch_related(
                            Prefetch("creador_proyecto"),
                            Prefetch("colaboradores_proyecto"),
                            Prefetch("creador_tarea"),
                            Prefetch("comentarios_creador"),
                               )
                        .filter(asignaciontarea=None)
    ).all()
    return render(request, "usuario/lista_completa_no_asignados.html", {"usuarios":usuarios})
    
   
        
"""
    Crear una página de Error personalizada para cada uno de los 4 tipos de errores 
    que pueden ocurrir en nuestra Web.
"""
#Páginas de Error
def mi_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)
