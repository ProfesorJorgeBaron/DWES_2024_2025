from django.contrib import admin
from .models import Biblioteca,Libro,Autor,Cliente,DatosCliente,Prestamo

# Register your models here.
admin.site.register(Biblioteca)
admin.site.register(Libro)
admin.site.register(Autor)
admin.site.register(Cliente)
admin.site.register(DatosCliente)
admin.site.register(Prestamo)