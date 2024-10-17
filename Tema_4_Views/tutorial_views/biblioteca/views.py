from django.shortcuts import render
from django.db.models import Q,F,Prefetch
from django.db.models import Avg,Max,Min
from .models import Libro,Cliente,Biblioteca


# Create your views here.
def index(request):
    return render(request, 'index.html') 

#Una url que me muestre todos los libros y sus datos, incluido los relacionados
def listar_libros(request):
    libros = Libro.objects.select_related("biblioteca").prefetch_related("autores")
    libros = libros.all()
    """libros = (Libro.objects.raw("SELECT * FROM biblioteca_libro l "
                               + " JOIN biblioteca_biblioteca b ON l.biblioteca_id = b.id " 
                               + " JOIN biblioteca_libro_autores la ON la.libro_id = l.id ")
             )
    """
    return render(request, 'libro/lista.html',{"libros_mostrar":libros})

#Una url que me muestre información sobre cada libro
def dame_libro(request,id_libro):
    QSlibro = Libro.objects.select_related("biblioteca").prefetch_related("autores")
    libro = QSlibro.get(id=id_libro)
    
    """libro = (Libro.objects.raw("SELECT * FROM biblioteca_libro l "
                               + " JOIN biblioteca_biblioteca b ON l.biblioteca_id = b.id " 
                               + " JOIN biblioteca_libro_autores la ON la.libro_id = l.id "
                               + " WHERE l.id = %s",[id_libro])[0]
             )
    """
    
    return render(request, 'libro/libro.html',{"libro_mostrar":libro})

#Una url que me muestre los libros de un año y mes concreto
def dame_libros_fecha(request,anyo_libro,mes_libro):
    libros = Libro.objects.prefetch_related("autores").select_related("biblioteca")
    libros = libros.filter(fecha_publicacion__year=anyo_libro,fecha_publicacion__month=mes_libro)
    
    """libros = (Libro.objects.raw("SELECT * FROM biblioteca_libro l "
                               + " JOIN biblioteca_libro_autores la ON la.libro_id = l.id "
                               + " JOIN biblioteca_biblioteca b ON l.biblioteca_id = b.id " 
                               + " WHERE strftime('%%Y', l.fecha_publicacion) = %s "
                               + " AND strftime('%%m', l.fecha_publicacion) = %s "
                               ,[str(anyo_libro),str(mes_libro)])
             )
    """
     
    return render(request, 'libro/lista.html',{"libros_mostrar":libros})

#Una url que me muestre los libros que tienen el idioma del libro o español ordenados por fecha de publicación
def dame_libros_idioma(request,idioma):
    libros = Libro.objects.select_related("biblioteca").prefetch_related("autores")
    libros = libros.filter(Q(idioma=idioma) | Q(idioma="ES")).order_by("fecha_publicacion")
    
    """libros = (Libro.objects.raw("SELECT * FROM biblioteca_libro l "
                               + " JOIN biblioteca_biblioteca b ON l.biblioteca_id = b.id "   
                               + " JOIN biblioteca_libro_autores la ON la.libro_id = l.id "
                               + " WHERE idioma = 'ES' "
                               + " OR idioma = %s "
                               + " ORDER BY l.fecha_publicacion"
                               ,[idioma])
               )
    """
    
    
    return render(request, 'libro/lista.html',{"libros_mostrar":libros})

#Una url que me muestre los libros de una biblioteca que contenga un texto en concreto.
def dame_libros_biblioteca(request,id_biblioteca,texto_libro):
    libros = Libro.objects.select_related("biblioteca").prefetch_related("autores")
    libros = libros.filter(biblioteca=id_biblioteca).filter(descripcion__contains=texto_libro).order_by("-nombre")
    
    """texto_buscar = "'%"+texto_libro+"%'"
    libros = (Libro.objects.raw("SELECT * FROM biblioteca_libro l "
                               + " JOIN biblioteca_biblioteca b ON l.biblioteca_id = b.id "   
                               + " JOIN biblioteca_libro_autores la ON la.libro_id = l.id "
                               + " WHERE b.id = %s "
                               + " AND l.descripcion LIKE %s "
                               + " ORDER BY l.nombre DESC "
                               ,[id_biblioteca,texto_buscar])
               )
    """
  
    return render(request, 'libro/lista.html',{"libros_mostrar":libros})

#Una url que me muestre el último cliente que se llevó un libro en concreto
def dame_ultimo_cliente_libro(request,libro):
    cliente = Cliente.objects.filter(prestamo__libro=libro).order_by("-prestamo__fecha_prestamo")[:1].get()
    cliente = (Cliente.objects.raw("SELECT * FROM biblioteca_cliente c "
                               + " JOIN biblioteca_prestamo p ON p.libro_id = %s "   
                               + " ORDER BY p.fecha_prestamo DESC "
                               ,[libro])[0]
               )
    
    return  render(request, 'cliente/cliente.html',{"cliente":cliente})

#Una url que muestre los libros que nunca han sido prestados.
def libros_no_prestados(request):
    libros = Libro.objects.select_related("biblioteca").prefetch_related("autores")
    libros = libros.filter(prestamo=None)
    
    """libros = (Libro.objects.raw("SELECT * FROM biblioteca_libro l "
                               + " JOIN biblioteca_biblioteca b ON l.biblioteca_id = b.id "   
                               + " JOIN biblioteca_libro_autores la ON la.libro_id = l.id "
                               + " LEFT JOIN biblioteca_prestamo p ON p.libro_id = l.id "
                               + " WHERE p.id IS NULL ")
            ) 
    """
    
    return render(request, 'libro/lista.html',{"libros_mostrar":libros})

#Una url que muestre una página con una Biblioteca y sus libros
def dame_biblioteca(request,id_biblioteca):
    biblioteca = Biblioteca.objects.prefetch_related(Prefetch("libros_biblioteca")).get(id=id_biblioteca)
    
    """biblioteca = (Biblioteca.objects.raw("SELECT * FROM biblioteca_biblioteca b "
                               + " JOIN biblioteca_libro l ON l.biblioteca_id = b.id "   
                              ) 
            )[0] 
    """
    return render(request, 'biblioteca/biblioteca.html',{"biblioteca":biblioteca})

#Una url que muestre los libros que contengan en la descripcion el titulo del libro
def dame_libros_titulo_en_descripcion(request):
    libros = Libro.objects.select_related("biblioteca").prefetch_related("autores")
    libros = libros.filter(descripcion__contains=F("nombre"))
  
    return render(request, 'libro/lista.html',{"libros_mostrar":libros})

#Una url que muestra la media, máximo y  mínimo de puntos de todos los clientes de la Biblioteca
def dame_agrupaciones_puntos_cliente(request):
    resultado = Cliente.objects.aggregate(Avg("puntos"),Max("puntos"),Min("puntos"))
    media = resultado["puntos__avg"]
    maximo = resultado["puntos__max"]
    minimo = resultado["puntos__min"]
    return render(request, 'cliente/agrupaciones.html',{"media":media,"maximo":maximo,"minimo":minimo})            

#Páginas de Error
def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)