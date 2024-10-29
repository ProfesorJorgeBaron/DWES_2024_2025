from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Proyecto)
admin.site.register(Tarea)
admin.site.register(AsignacionTarea)
admin.site.register(Etiqueta)
admin.site.register(Comentario)