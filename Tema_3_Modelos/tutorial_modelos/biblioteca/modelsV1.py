from django.db import models

# Create your models here.

class Biblioteca(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=200,blank=True)
    edad = models.IntegerField(null = True)
    
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
    biblioteca = models.ForeignKey(Biblioteca,on_delete=models.CASCADE)
    autores = models.ManyToManyField(Autor)

    
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.CharField(max_length=200,unique=True)
    puntos = models.FloatField(default=5.0,db_column = "puntos_biblioteca")
    
class DatosCliente(models.Model):
     direccion = models.TextField()
     gustos = models.TextField()
     telefono = models.IntegerField()
     cliente = models.OneToOneField(Cliente,on_delete=models.CASCADE)