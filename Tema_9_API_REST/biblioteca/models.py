from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.

        
class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    CLIENTE = 2
    BIBLIOTECARIO = 3
    ROLES = (
        (ADMINISTRADOR, 'administardor'),
        (CLIENTE, 'cliente'),
        (BIBLIOTECARIO, 'bibliotecario'),
    )
    
    rol  = models.PositiveSmallIntegerField(
        choices=ROLES,default=1
    )


class Bibliotecario(models.Model):
    usuario = models.OneToOneField(Usuario, 
                             on_delete = models.CASCADE)

class Biblioteca(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    
    creador = models.ForeignKey(Bibliotecario, on_delete = models.CASCADE,related_name="creador_biblioteca")
    
    def __str__(self):
        return self.nombre

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=200,blank=True)
    edad = models.IntegerField(null = True)
    
    def __str__(self):
        return self.nombre + " "+ self.apellidos


class Categoria(models.Model):
    categoria = models.CharField(max_length=200)
    
    def __str__(self):
        return self.categoria

    
class Libro(models.Model):
    IDIOMAS = [
        ("ES", "Español"),
        ("EN", "Inglés"),
        ("FR", "Francés"),
        ("IT", "Italiano"),
    ]

    nombre = models.CharField(max_length=200)
    idioma = models.CharField(
        max_length=2,
        choices=IDIOMAS,
        default="ES",
    )
    
    descripcion = models.TextField()
    fecha_publicacion = models.DateField()
    fecha_actualizacion = models.DateTimeField(default=timezone.now,blank=True)
    biblioteca = models.ForeignKey(Biblioteca, on_delete = models.CASCADE,related_name="libros_biblioteca")
    autores =  models.ManyToManyField(Autor,related_name="libros_autores")
    categorias = models.ManyToManyField(Categoria,through="LibrosCategorias")
    imagen = models.FileField(null=True)

    def __str__(self):
        return self.nombre
    

class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, 
                             on_delete = models.CASCADE)
    puntos = models.FloatField(default=5.0,db_column = "puntos_biblioteca")
    libros = models.ManyToManyField(Libro, through='Prestamo',related_name='prestamos_libros')

    def __str__(self):
        return self.usuario.username


class DatosCliente(models.Model):
     cliente = models.OneToOneField(Cliente, 
                             on_delete = models.CASCADE)
     direccion = models.TextField()
     gustos = models.TextField()
     telefono = models.IntegerField()


class Prestamo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField(default=timezone.now,blank=True)

class LibrosCategorias(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    