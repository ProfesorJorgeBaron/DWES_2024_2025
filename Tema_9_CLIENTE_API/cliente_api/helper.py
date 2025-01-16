
import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()


class helper:

    def obtener_bibliotecas_select():
        # obtenemos todos los libros
        headers = {'Authorization': 'Bearer '+env("TOKEN_ACCESO")} 
        response = requests.get('http://127.0.0.1:8000/api/v1/bibliotecas',headers=headers)
        bibliotecas = response.json()
        
        lista_bibliotecas = [("","Ninguna")]
        for biblioteca in bibliotecas:
            lista_bibliotecas.append((biblioteca["id"],biblioteca["nombre"]))
        return lista_bibliotecas

    def obtener_autores_select():
        # obtenemos todos los libros
        headers = {'Authorization': 'Bearer '+env("TOKEN_ACCESO")} 
        response = requests.get('http://127.0.0.1:8000/api/v1/autores',headers=headers)
        autores = response.json()
        lista_autores = []
        for autor in autores:
            lista_autores.append((autor["id"],autor["nombre"]))
        return lista_autores
    
    def obtener_categorias_select():
        # obtenemos todos los libros
        headers = {'Authorization': 'Bearer '+env("TOKEN_ACCESO")} 
        response = requests.get('http://127.0.0.1:8000/api/v1/categorias',headers=headers)
        categorias = response.json()
        lista_categorias = []
        for categoria in categorias:
            lista_categorias.append((categoria["id"],categoria["categoria"]))
        return lista_categorias
    
    def obtener_libro(id):
         # obtenemos todos los libros
        headers = {'Authorization': 'Bearer '+env("TOKEN_ACCESO")} 
        response = requests.get('http://127.0.0.1:8000/api/v1/libro/'+str(id),headers=headers)
        libro = response.json()
        return libro
    
    def obtener_token_session(usuario,password):
        token_url = 'http://127.0.0.1:8000/oauth2/token/'
        data = {
            'grant_type': 'password',
            'username': usuario,
            'password': password,
            'client_id': 'biblioteca',
            'client_secret': 'biblioteca',
        }

        response = requests.post(token_url, data=data)
        respuesta = response.json()
        if response.status_code == 200:
            return respuesta.get('access_token')
        else:
            raise Exception(respuesta.get("error_description"))
        
    def clasificar_texto(text):
        key = "543401d0-c982-11ee-8c3f-15f879bf0d6e9c43b3af-55a3-4803-8cf8-f424b47f9366"
        url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

        response = requests.get(url, params={ "data" : text })

        if response.ok:
            responseData = response.json()
            topMatch = responseData[0]
            return topMatch
        else:
            response.raise_for_status()