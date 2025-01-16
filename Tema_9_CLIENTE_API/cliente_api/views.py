from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from .helper import helper
import json
from requests.exceptions import HTTPError

import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()

# Create your views here.
#Vistas API


# Create your views here.
def index(request):
    return render(request, 'index.html')

def crear_cabecera():
    return {
        'Authorization': 'Bearer '+env("TOKEN_ACCESO"),
        "Content-Type": "application/json"
        }

def libros_lista(request):
    # obtenemos todos los libros
    #headers = {'Authorization': 'Bearer SlNWDzValrcSZ2QGrI8Nx3lFwEKTou'} 
    headers = {'Authorization': 'Bearer '+request.session["token"]} 
    print(headers)
    response = requests.get('http://127.0.0.1:8000/api/v1/libros',headers=headers)
   # Transformamos la respuesta en json
    libros = response.json()
    #return render(request, 'libro/lista.html',{"libros_mostrar":libros})
    return render(request, 'libro/lista_mejorada.html',{"libros_mostrar":libros})


def libro_busqueda_simple(request):
    formulario = BusquedaLibroForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera()
        response = requests.get(
            'http://127.0.0.1:8000/api/v1/libros/busqueda_simple',
            headers=headers,
            params={'textoBusqueda':formulario.data.get("textoBusqueda")}
        )
        libros = response.json()
        return render(request, 'libro/lista_mejorada.html',{"libros_mostrar":libros})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    

def libro_busqueda_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaLibroForm(request.GET)
        
        try:
            headers = crear_cabecera()
            response = requests.get(
                'http://127.0.0.1:8000/api/v1/libros/busqueda_avanzada',
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                libros = response.json()
                return render(request, 'libro/lista_mejorada.html',
                              {"libros_mostrar":libros})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'libro/busqueda_avanzada.html',
                            {"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaLibroForm(None)
    return render(request, 'libro/busqueda_avanzada.html',{"formulario":formulario})

import base64

def libro_crear(request):
    
    if (request.method == "POST"):
        try:
            formulario = LibroForm(request.POST)
            headers =  {
                        'Authorization': 'Bearer '+env("TOKEN_ACCESO"),
                        "Content-Type": "application/json" 
                    } 
            datos = formulario.data.copy()
            datos["autores"] = request.POST.getlist("autores");
            datos["categorias"] = request.POST.getlist("categorias")
            datos["fecha_publicacion"] = str(
                                            datetime.date(year=int(datos['fecha_publicacion_year']),
                                                        month=int(datos['fecha_publicacion_month']),
                                                        day=int(datos['fecha_publicacion_day']))
                                             )
             
            imagen = request.FILES["imagen"].read()
            datos["imagen"] = base64.b64encode(imagen).decode('utf-8')
            #imagen = request.FILES['imagen'].file.getvalue()
            #imagenes = {'imagen': imagen}

            
            response = requests.post(
                'http://127.0.0.1:8000/api/v1/libros/crear',
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("libro_lista")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'libro/create.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
        
    else:
         formulario = LibroForm(None)
    return render(request, 'libro/create.html',{"formulario":formulario})


def libro_obtener(request,libro_id):
    libro = helper.obtener_libro(libro_id)
    return render(request, 'libro/libro_mostrar.html',{"libro":libro})


from .cliente_api import cliente_api
def libro_editar(request,libro_id):
   
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    libro = helper.obtener_libro(libro_id)
    formulario = LibroForm(datosFormulario,
            initial={
                'nombre': libro['nombre'],
                'descripcion': libro["descripcion"],
                'fecha_publicacion': datetime.datetime.strptime(libro['fecha_publicacion'], '%d-%m-%Y').date(),
                'idioma': libro['idioma'],
                'biblioteca': libro['biblioteca']['id'],
                'autores': [autor['id'] for autor in libro['autores']],
                'categorias': [categoria['categoria']["id"] for categoria in libro['categorias']]
            }
    )
    if (request.method == "POST"):
        formulario = LibroForm(request.POST)
        datos = request.POST.copy()
        datos["autores"] = request.POST.getlist("autores")
        datos["categorias"] = request.POST.getlist("categorias")
        datos["fecha_publicacion"] = str(datetime.date(year=int(datos['fecha_publicacion_year']),
                                                    month=int(datos['fecha_publicacion_month']),
                                                    day=int(datos['fecha_publicacion_day'])))
        
        
        cliente = cliente_api(request.session["token"],"PUT",'libros/editar/'+str(libro_id),datos)
        cliente.realizar_peticion_api()
        if(cliente.es_respuesta_correcta()):
            return redirect("libro_mostrar",libro_id=libro_id)
        else:
            if(cliente.es_error_validacion_datos()):
                cliente.incluir_errores_formulario(formulario)
            else:
                return tratar_errores(request,cliente.codigoRespuesta)
    return render(request, 'libro/actualizar.html',{"formulario":formulario,"libro":libro})


def libro_editar_nombre(request,libro_id):
   
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    libro = helper.obtener_libro(libro_id)
    formulario = LibroActualizarNombreForm(datosFormulario,
            initial={
                'nombre': libro['nombre'],
            }
    )
    if (request.method == "POST"):
        try:
            formulario = LibroActualizarNombreForm(request.POST)
            headers = crear_cabecera()
            datos = request.POST.copy()
            response = requests.patch(
                'http://127.0.0.1:8000/api/v1/libros/actualizar/nombre/'+str(libro_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("libro_mostrar",libro_id=libro_id)
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'libro/actualizar_nombre.html',
                            {"formulario":formulario,"libro":libro})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'libro/actualizar_nombre.html',{"formulario":formulario,"libro":libro})
    

def libro_eliminar(request,libro_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(
            'http://127.0.0.1:8000/api/v1/libros/eliminar/'+str(libro_id),
            headers=headers,
        )
        if(response.status_code == requests.codes.ok):
            return redirect("libro_lista")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('libro_lista')


def registrar_usuario(request):
    if (request.method == "POST"):
        try:
            formulario = RegistroForm(request.POST)
            if(formulario.is_valid()):
                headers =  {
                            "Content-Type": "application/json" 
                        }
                response = requests.post(
                    'http://127.0.0.1:8000/api/v1/registrar/usuario',
                    headers=headers,
                    data=json.dumps(formulario.cleaned_data)
                )
                
                if(response.status_code == requests.codes.ok):
                    usuario = response.json()
                    token_acceso = helper.obtener_token_session(
                            formulario.cleaned_data.get("username"),
                            formulario.cleaned_data.get("password1")
                            )
                    request.session["usuario"]=usuario
                    request.session["token"] = token_acceso
                    redirect("index")
                else:
                    print(response.status_code)
                    response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'registration/signup.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
            
    else:
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})

def login(request):
    if (request.method == "POST"):
        formulario = LoginForm(request.POST)
        try:
            token_acceso = helper.obtener_token_session(
                                formulario.data.get("usuario"),
                                formulario.data.get("password")
                                )
            request.session["token"] = token_acceso
            
          
            headers = {'Authorization': 'Bearer '+token_acceso} 
            response = requests.get('http://127.0.0.1:8000/api/v1/usuario/token/'+token_acceso,headers=headers)
            usuario = response.json()
            request.session["usuario"] = usuario
            
            return  redirect("index")
        except Exception as excepcion:
            print(f'Hubo un error en la petición: {excepcion}')
            formulario.add_error("usuario",excepcion)
            formulario.add_error("password",excepcion)
            return render(request, 
                            'registration/login.html',
                            {"form":formulario})
    else:  
        formulario = LoginForm()
    return render(request, 'registration/login.html', {'form': formulario})


    
def logout(request):
    del request.session['token']
    return redirect('index')


def tratar_errores(request,codigo):
    if codigo == 404:
        return mi_error_404(request)
    else:
        return mi_error_500(request)
        


#Páginas de Error
def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

#Páginas de Error
def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)

