from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework import status
from .forms import *
from django.db.models import Q,Prefetch
from django.contrib.auth.models import Group
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .cliente_ml import cliente_ml

@api_view(['GET'])
def libro_list(request):
    libros = Libro.objects.select_related("biblioteca").prefetch_related("autores").all()
    #serializer = LibroSerializer(libros, many=True)
    serializer = LibroSerializerMejorado(libros, many=True)
    return Response(serializer.data)
    
@api_view(['GET'])
def cliente_list(request):
    clientes = Cliente.objects.all()
    serializer = ClienteSerializer(clientes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def libro_buscar(request):
    formulario = BusquedaLibroForm(request.query_params)
    if(formulario.is_valid()):
        texto = formulario.data.get('textoBusqueda')
        libros = Libro.objects.select_related("biblioteca").prefetch_related("autores")
        libros = libros.filter(Q(nombre__contains=texto) | Q(descripcion__contains=texto)).all()
        serializer = LibroSerializerMejorado(libros, many=True)
        return Response(serializer.data)
    else:
        return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
   

@api_view(['GET'])
def libro_buscar_avanzado(request):

    if(len(request.query_params) > 0):
        formulario = BusquedaAvanzadaLibroForm(request.query_params)
        if formulario.is_valid():
            texto = formulario.cleaned_data.get('textoBusqueda')
            QSlibros = Libro.objects.select_related("biblioteca").prefetch_related("autores","categorias")
           
            #obtenemos los filtros
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            textoCategoria = formulario.cleaned_data.get('textoCategoria')
            idiomas = formulario.cleaned_data.get('idiomas')
            fechaDesde = formulario.cleaned_data.get('fecha_desde')
            fechaHasta = formulario.cleaned_data.get('fecha_hasta')
            
            #Por cada filtro comprobamos si tiene un valor y lo añadimos a la QuerySet
            if(textoBusqueda != ""):
                QSlibros = QSlibros.filter(Q(nombre__contains=texto) | Q(descripcion__contains=texto))
                
                
                
            #Si hay idiomas, iteramos por ellos, creamos la queryOR y le aplicamos el filtro
            if(len(idiomas) > 0):
                filtroOR = Q(idioma=idiomas[0])
                for idioma in idiomas[1:]:
                    mensaje_busqueda += " o "+idiomas[1]
                    filtroOR |= Q(idioma=idioma)
                QSlibros =  QSlibros.filter(filtroOR)
            
            #Comprobamos fechas
            #Obtenemos los libros con fecha publicacion mayor a la fecha desde
            if(not fechaDesde is None):
                QSlibros = QSlibros.filter(fecha_publicacion__gte=fechaDesde)
            
             #Obtenemos los libros con fecha publicacion menor a la fecha desde
            if(not fechaHasta is None):
                QSlibros = QSlibros.filter(fecha_publicacion__lte=fechaHasta)
            
            
            if(textoCategoria != ""):
                resultado = cliente_ml.clasificar(textoCategoria)
                if(resultado['confidence']) > 60:
                    QSlibros = QSlibros.filter(categorias__categoria=resultado["class_name"])
            
            
            libros = QSlibros.all()
            serializer = LibroSerializerMejorado(libros, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
  
@api_view(['GET'])
def biblioteca_list(request):
    bibliotecas = Biblioteca.objects.all()
    serializer = BibliotecaSerializer(bibliotecas, many=True)
    return Response(serializer.data)
    
@api_view(['GET'])
def autor_list(request):
    autores = Autor.objects.all()
    serializer = AutorSerializer(autores, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def categoria_list(request):
    categorias = Categoria.objects.all()
    serializer = CategoriaSerializer(categorias, many=True)
    return Response(serializer.data)

'''
@api_view(['POST'])
def libro_create(request):
    formulario = LibroModelForm(request.query_params)
    if formulario.is_valid():
        try:
            formulario.save()
            return Response("Libro CREADO")
        except Exception as error:
            print(error)
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
'''

@api_view(['POST'])
def libro_create(request): 
    print(request.data)
    libroCreateSerializer = LibroSerializerCreate(data=request.data)
    if libroCreateSerializer.is_valid():
        try:
            libroCreateSerializer.save()
            return Response("Libro CREADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(libroCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET']) 
def libro_obtener(request,libro_id):
    libro = Libro.objects.select_related("biblioteca").prefetch_related("autores")
    libro = libro.get(id=libro_id)
    serializer = LibroSerializerMejorado(libro)
    return Response(serializer.data)

@api_view(['PUT'])
def libro_editar(request,libro_id):
    libro = Libro.objects.get(id=libro_id)
    libroCreateSerializer = LibroSerializerCreate(data=request.data,instance=libro)
    if libroCreateSerializer.is_valid():
        try:
            libroCreateSerializer.save()
            return Response("Libro EDITADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(libroCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def libro_actualizar_nombre(request,libro_id):
    libro = Libro.objects.get(id=libro_id)
    serializers = LibroSerializerActualizarNombre(data=request.data,instance=libro)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Libro EDITADO")
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def libro_eliminar(request,libro_id):
    libro = Libro.objects.get(id=libro_id)
    try:
        libro.delete()
        return Response("Libro ELIMINADO")
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny

class registrar_usuario(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegistro
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializers = UsuarioSerializerRegistro(data=request.data)
        if serializers.is_valid():
            try:
                rol = request.data.get('rol')
                user = Usuario.objects.create_user(
                        username = serializers.data.get("username"), 
                        email = serializers.data.get("email"), 
                        password = serializers.data.get("password1"),
                        rol = rol,
                        )
                if(rol == Usuario.CLIENTE):
                    grupo = Group.objects.get(name='Clientes') 
                    grupo.user_set.add(user)
                    cliente = Cliente.objects.create( usuario = user)
                    cliente.save()
                elif(rol == Usuario.BIBLIOTECARIO):
                    grupo = Group.objects.get(name='Bibliotecarios') 
                    grupo.user_set.add(user)
                    bibliotecario = Bibliotecario.objects.create(usuario = user)
                    bibliotecario.save()
                usuarioSerializado = UsuarioSerializer(user)
                return Response(usuarioSerializado.data)
            except Exception as error:
                print(repr(error))
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


from oauth2_provider.models import AccessToken     
@api_view(['GET'])
def obtener_usuario_token(request,token):
    ModeloToken = AccessToken.objects.get(token=token)
    usuario = Usuario.objects.get(id=ModeloToken.user_id)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)
    

    