from rest_framework import serializers
from .models import *
from .forms import *
                
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


class BibliotecarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bibliotecario
        fields = '__all__'
    
class BibliotecaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biblioteca
        fields = '__all__'
    
class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'
    
class LibroSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Libro


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'
        

class LibrosCategoriasSerializer(serializers.ModelSerializer):
    
    categoria = CategoriaSerializer()
    
    class Meta:
        model = LibrosCategorias
        fields = '__all__'

class LibroSerializerMejorado(serializers.ModelSerializer):
   
    #Para relaciones ManyToOne o OneToOne
    biblioteca = BibliotecaSerializer()
    
    #Para las relaciones ManyToMany
    autores = AutorSerializer(read_only=True, many=True)
    
    #Para las relaciones ManyToMany con through
    categorias = LibrosCategoriasSerializer(read_only=True, many=True,source='libroscategorias_set')
    
    #Para formatear Fechas
    fecha_publicacion = serializers.DateField(format=('%d-%m-%Y'))
    
    #Para obtener el valor de un Choice
    idioma = serializers.CharField(source='get_idioma_display')
    
    class Meta:
        fields = ('id',
                  'nombre',
                  'idioma',
                  'descripcion',
                  'fecha_publicacion',
                  'biblioteca',
                  'autores',
                  'categorias'
                  )
        model = Libro

class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = '__all__'


class ClienteSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    libros = PrestamoSerializer(read_only=True,source="prestamo_set",many=True)
    
    class Meta:
        model = Cliente
        fields = '__all__'


class DatosClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosCliente
        fields = '__all__'
        

import base64
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

class LibroSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Libro
        fields = ['nombre','descripcion','fecha_publicacion',
                  'idioma','biblioteca','autores',
                  'fecha_actualizacion',
                  'categorias']
    
    def validate_nombre(self,nombre):
        libroNombre = Libro.objects.filter(nombre=nombre).first()
        if(not libroNombre is None
           ):
             if(not self.instance is None and libroNombre.id == self.instance.id):
                 pass
             else:
                raise serializers.ValidationError('Ya existe un libro con ese nombre')
            
        
        return nombre
    
    def validate_descripcion(self,descripcion):
        if len(descripcion) < 10:
             raise serializers.ValidationError('Al menos debes indicar 10 caracteres')
        return descripcion
    
    def validate_fecha_publicacion(self,fecha_publicacion):
        fechaHoy = date.today()
        if fechaHoy >= fecha_publicacion:
            raise serializers.ValidationError('La fecha de publicacion debe ser mayor a Hoy')
        return fecha_publicacion
    
    def validate_biblioteca(self,biblioteca): 
        if self.initial_data['idioma'] == "FR" and biblioteca == 1:
            raise serializers.ValidationError('No puede usar la Biblioteca de la Universidad de Sevilla y el idioma Fránces')
        return biblioteca
    
    def validate_idioma(self,idioma): 
        if idioma == "FR" and int(self.initial_data['biblioteca']) == 1:
            raise serializers.ValidationError('No puede usar la Biblioteca de la Universidad de Sevilla y el idioma Fránces')
        return idioma
    
    def validate_autores(self,autores):
        if len(autores) < 1:
            raise serializers.ValidationError('Debe seleccionar al menos un autor')
        return autores
    
    def create(self, validated_data):
        categorias = self.initial_data['categorias']
        imagen =  base64.b64decode(self.initial_data['imagen'])
        contenido_archivo = ContentFile(imagen)
        
        archivo = InMemoryUploadedFile(
            contenido_archivo,       
            None,               
            validated_data["nombre"],     
            'image/jpeg',     
            contenido_archivo.size,   
            None
        )
        
        if len(categorias) < 2:
            raise serializers.ValidationError(
                    {'categorias':
                    ['Debe seleccionar al menos dos categorias']
                    })
        
        libro = Libro.objects.create(
            nombre = validated_data["nombre"],
            descripcion = validated_data["descripcion"],
            fecha_publicacion = validated_data["fecha_publicacion"],
            idioma = validated_data["idioma"],
            biblioteca = validated_data["biblioteca"],
            imagen=archivo
        )
        libro.autores.set(validated_data["autores"])
       
        for categoria in categorias:
            modeloCategoria = Categoria.objects.get(id=categoria)
            LibrosCategorias.objects.create(categoria=modeloCategoria,libro=libro)
        return libro
    
    def update(self, instance, validated_data):
        categorias = self.initial_data['categorias']
        if len(categorias) < 2:
            raise serializers.ValidationError(
                    {'categorias':
                    ['Debe seleccionar al menos dos categorias']
                    })
        
        instance.nombre = validated_data["nombre"]
        instance.descripcion = validated_data["descripcion"]
        instance.fecha_publicacion = validated_data["fecha_publicacion"]
        instance.idioma = validated_data["idioma"]
        instance.biblioteca = validated_data["biblioteca"]
        instance.save()
        
        instance.autores.set(validated_data["autores"])

        instance.categorias.clear()
        for categoria in categorias:
            modeloCategoria = Categoria.objects.get(id=categoria)
            LibrosCategorias.objects.create(categoria=modeloCategoria,libro=instance)
        return instance

class LibroSerializerActualizarNombre(serializers.ModelSerializer):
 
    class Meta:
        model = Libro
        fields = ['nombre']
    
    def validate_nombre(self,nombre):
        libroNombre = Libro.objects.filter(nombre=nombre).first()
        if(not libroNombre is None and libroNombre.id != self.instance.id):
            raise serializers.ValidationError('Ya existe un libro con ese nombre')
        return nombre
    
class UsuarioSerializerRegistro(serializers.Serializer):
 
    username = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    email = serializers.EmailField()
    rol = serializers.IntegerField()
    
    def validate_username(self,username):
        usuario = Usuario.objects.filter(username=username).first()
        if(not usuario is None):
            raise serializers.ValidationError('Ya existe un usuario con ese nombre')
        return username