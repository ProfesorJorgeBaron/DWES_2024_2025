from django.conf import settings
from django.db import models
from django.utils import timezone
# Create your models here.

class Usuario(models.Model):
    nombre=models.CharField(max_length=50)
    email=models.CharField(max_length=100,unique=True)
    password=models.CharField(max_length=20)
    fecha_registro=models.DateTimeField(default=timezone.now)

class Proyecto(models.Model):
    nombre=models.CharField(max_length=100)
    descripcion=models.TextField(max_length=2500) 
    duracion=models.FloatField()
    fecha_inicio=models.DateField(default=timezone.now)
    fecha_fin=models.DateField(default=timezone.now)
    
    """
        Relación con Proyecto (Proyectos Asignados): 
        Un usuario puede estar asignado a varios proyectos como colaborador.
        Y un proyecto puede tener varios usuarios.
    """
    colaboradores=models.ManyToManyField(Usuario,related_name='colaboradores_proyecto')
    
    """
        Relación con Usuario (Creador): Un proyecto tiene un usuario que lo crea o administra. 
    """
    creador=models.ForeignKey(Usuario,related_name='creador_proyecto',on_delete=models.CASCADE)
    
class Tarea(models.Model):
    titulo=models.CharField(max_length=100) 
    descripcion=models.TextField()
    prioridad=models.IntegerField()
    
    ESTADOS=[('PE','Pendiente'),('PR','Progreso'),('Co','Completada')]
    estado=models.CharField(max_length=2,choices=ESTADOS)
    
    completada=models.BooleanField()
    fecha_creacion=models.DateField(default=timezone.now)
    hora_vencimiento=models.TimeField(default=timezone.now)
    
    """
        Relación con Usuario (Creador): 
        Muchas tareas pueden ser creadas por un usuario. 
    """
    creador=models.ForeignKey(Usuario,on_delete=models.CASCADE,related_name="creador_tarea")
    
    
    """
        Relación con usuarios(usuarios asignados): Una tarea puede tener asignado uno o más usuarios 
        y un usuario puede estar en varias tareas, 
        por lo tanto vamos a relacionarlos a través de una tabla intermedia Asignación de Tarea.
    """
    usuarios_asignados=models.ManyToManyField(Usuario, through='asignacionTarea',
                                            related_name='colaboradores_tarea')
    
    """
        Relación con Proyecto (proyecto): Un proyecto tiene varias tareas creadas, 
        para desarrollar el proyecto.
    """
    proyecto=models.ForeignKey(Proyecto,on_delete=models.CASCADE,related_name="proyecto_tareas")

class AsignacionTarea(models.Model):
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE)
    tarea=models.ForeignKey(Tarea,on_delete=models.CASCADE)
    observaciones=models.TextField(max_length=2500)
    fecha_asignacion=models.DateTimeField(default=timezone.now)

class Etiqueta(models.Model):
    nombre=models.CharField(max_length=30,unique=True)
    
    """
        Relación con Etiqueta (Etiquetas Asociadas): Una tarea puede tener varias etiquetas. 
        Y una etiqueta puede estar asignada a varias tareas.
    """
    tarea=models.ManyToManyField(Tarea,related_name="etiquetas_tareas")

class Comentario(models.Model):
    contenido=models.TextField(max_length=2500)
    fecha_comentario=models.DateTimeField(default=timezone.now)
    
    """
        Relación con Usuario (Autor): Cada comentario tiene un autor (usuario). 
    """
    autor=models.ForeignKey(Usuario,on_delete=models.CASCADE,related_name="comentarios_creador")
    
    """
        Relación con Tarea: Cada comentario está asociado a una tarea. 
    """
    tarea=models.ForeignKey(Tarea,on_delete=models.CASCADE,related_name="comentarios_tarea")