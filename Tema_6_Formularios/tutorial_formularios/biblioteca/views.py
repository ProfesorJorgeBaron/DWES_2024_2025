from django.shortcuts import render,redirect
from django.db.models import Q,Prefetch
from django.forms import modelform_factory
from .models import *
from .forms import *
from django.contrib import messages

from datetime import datetime

# Create your views here.
def index(request):
    return render(request, 'index.html') 

def libro_create_sencillo(request):
    
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = LibroModelForm(datosFormulario)
    if (request.method == "POST"):
        if formulario.is_valid():
            try:
                # Guarda el libro en la base de datos
                formulario.save()
                return redirect("libro_lista")
            except Exception as error:
                print(error)
    
    return render(request, 'libro/create.html',{"formulario":formulario})  

#Esta funcion es igual que la anterior pero con el
# código estructurado de otra forma
def libro_create_sencillo2(request):
    if request.method == "POST":
        formulario = LibroModelForm(request.POST)
        if formulario.is_valid():
            try:
                # Guarda el libro en la base de datos
                formulario.save()
                return redirect("libro_lista")
            except Exception as error:
                print(error)
    else:
        formulario = LibroModelForm()
          
    return render(request, 'libro/create.html',{"formulario":formulario})  
  
   
def libro_create(request):
    
    # Si la petición es GET se creará el formulario Vacío
    # Si la petición es POST se creará el formulario con Datos.
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    
    #formulario = LibroForm(datosFormulario)
    formulario = LibroModelForm(datosFormulario)
    """formularioFactory = modelform_factory(Libro, 
                                            fields='__all__',
                                            widgets = {
                                                "fecha_publicacion":forms.SelectDateWidget()
                                            })
    formulario = formularioFactory(datosFormulario)"""
    
    if (request.method == "POST"):
        # Llamamos la función que creará el libro
        #libro_creado = crear_libro_generico(formulario)
        libro_creado = crear_libro_modelo(formulario)
        if(libro_creado):
             messages.success(request, 'Se ha creado el libro '+formulario.cleaned_data.get('nombre')+" correctamente")
             return redirect("libro_lista")
        
    return render(request, 'libro/create.html',{"formulario":formulario})


def crear_libro_generico(formulario):
    libro_creado = False
    # Comprueba si el formulario es válido
    if formulario.is_valid():
        
        # Obtiene los datos del formulario validados correctamente. 
        libro = Libro.objects.create(
                nombre = formulario.cleaned_data.get('nombre'),
                idioma = formulario.cleaned_data.get('idioma'),
                descripcion = formulario.cleaned_data.get('descripcion'),
                fecha_publicacion = formulario.cleaned_data.get('fecha_publicacion'),
                biblioteca = formulario.cleaned_data.get('biblioteca'),
        )
        
        #Añade los autores que son relaciones ManyToMany
        libro.autores.set(formulario.cleaned_data.get('autores'))
        try:
            # Guarda el libro en la base de datos
            libro.save()
            libro_creado = True
        except Exception as error:
            print(error)
    return libro_creado

def crear_libro_modelo(formulario):
    libro_creado = False
    # Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            # Guarda el libro en la base de datos
            formulario.save()
            libro_creado = True
        except Exception as error:
            print(error)
    return libro_creado
    
    
def libros_lista(request):
    libros = Libro.objects.select_related("biblioteca").prefetch_related("autores")
    libros = libros.all()
    return render(request, 'libro/lista.html',{"libros_mostrar":libros})


def libro_mostrar(request,libro_id):
    libro = Libro.objects.select_related("biblioteca").prefetch_related("autores")
    libro = libro.get(id=libro_id)
    return render(request, 'libro/libro_mostrar.html',{"libro":libro})

def libro_buscar(request):
    
    formulario = BusquedaLibroForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        libros = Libro.objects.select_related("biblioteca").prefetch_related("autores")
        libros = libros.filter(Q(nombre__contains=texto) | Q(descripcion__contains=texto)).all()
        mensaje_busqueda = "Se buscar por textos que contienen en su nombre o contenido la palabra: "+texto
        return render(request, 'libro/lista_busqueda.html',{"libros_mostrar":libros,"texto_busqueda":mensaje_busqueda})
    
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")

def libro_buscar_avanzado(request):

    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaLibroForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QSlibros = Libro.objects.select_related("biblioteca").prefetch_related("autores")
            
            #obtenemos los filtros
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            idiomas = formulario.cleaned_data.get('idiomas')
            fechaDesde = formulario.cleaned_data.get('fecha_desde')
            fechaHasta = formulario.cleaned_data.get('fecha_hasta')
            
            #Por cada filtro comprobamos si tiene un valor y lo añadimos a la QuerySet
            if(textoBusqueda != ""):
                QSlibros = QSlibros.filter(Q(nombre__contains=textoBusqueda) | Q(descripcion__contains=textoBusqueda))
                mensaje_busqueda +=" Nombre o contenido que contengan la palabra "+textoBusqueda+"\n"
            
            #Si hay idiomas, iteramos por ellos, creamos la queryOR y le aplicamos el filtro
            if(len(idiomas) > 0):
                mensaje_busqueda +=" El idioma sea "+idiomas[0]
                filtroOR = Q(idioma=idiomas[0])
                for idioma in idiomas[1:]:
                    mensaje_busqueda += " o "+idiomas[1]
                    filtroOR |= Q(idioma=idioma)
                mensaje_busqueda += "\n"
                QSlibros =  QSlibros.filter(filtroOR)
            
            #Comprobamos fechas
            #Obtenemos los libros con fecha publicacion mayor a la fecha desde
            if(not fechaDesde is None):
                mensaje_busqueda +=" La fecha sea mayor a "+datetime.strftime(fechaDesde,'%d-%m-%Y')+"\n"
                QSlibros = QSlibros.filter(fecha_publicacion__gte=fechaDesde)
            
             #Obtenemos los libros con fecha publicacion menor a la fecha desde
            if(not fechaHasta is None):
                mensaje_busqueda +=" La fecha sea menor a "+datetime.strftime(fechaHasta,'%d-%m-%Y')+"\n"
                QSlibros = QSlibros.filter(fecha_publicacion__lte=fechaHasta)
            
            libros = QSlibros.all()
    
            return render(request, 'libro/lista_busqueda.html',
                            {"libros_mostrar":libros,
                             "texto_busqueda":mensaje_busqueda})
    else:
        formulario = BusquedaAvanzadaLibroForm(None)
    return render(request, 'libro/busqueda_avanzada_datepicker.html',{"formulario":formulario})
  

def libro_editar(request,libro_id):
    libro = Libro.objects.get(id=libro_id)
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    
    formulario = LibroModelForm(datosFormulario,instance = libro)
    
    if (request.method == "POST"):
       
        if formulario.is_valid():
            try:  
                formulario.save()
                messages.success(request, 'Se ha editado el libro'+formulario.cleaned_data.get('nombre')+" correctamente")
                return redirect('libro_lista')  
            except Exception as error:
                print(error)
    return render(request, 'libro/actualizar.html',{"formulario":formulario,"libro":libro})
    

def libro_eliminar(request,libro_id):
    libro = Libro.objects.get(id=libro_id)
    try:
        libro.delete()
        messages.success(request, "Se ha elimnado el libro "+libro.nombre+" correctamente")
    except Exception as error:
        print(error)
    return redirect('libro_lista')
    
#Páginas de Error
def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)