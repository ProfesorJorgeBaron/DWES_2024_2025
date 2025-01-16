
import requests
import environ
import os
from pathlib import Path
import json
from requests.exceptions import HTTPError

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()


class cliente_api:
    
    token = ""
    metodo = ""
    url = ""
    datosEnvio = None
    formatoRespuesta = ""
    codigoRespuesta = 0
    datosRespuesta = {}
    headers = {}
    respuesta = None
    
    
    def __init__(self,token, metodo,url,datosEnvio=None,formatoRespuesta="json"):
        self.token = token        
        self.metodo = metodo   
        self.url = url
        self.datosEnvio = datosEnvio
        self.formatoRespuesta = formatoRespuesta
    
    def crear_cabecera(self):
        self.headers["Authorization"] = "Bearer "+self.token
        if(self.metodo == "PUT" or self.metodo == "PATCH" or self.metodo == "POST"):
            self.headers["Content-Type"] = "application/json"
    
    def transformar_datos_envio(self):
        if(self.datosEnvio is not None):
            self.datosEnvio=json.dumps(self.datosEnvio)
    
    def realizar_peticion(self):
        try:
            self.respuesta = requests.put(
                    env("URL")+self.url,
                    headers=self.headers,
                    data=self.datosEnvio
            )
            self.codigoRespuesta = self.respuesta.status_code
            self.respuesta.raise_for_status()
        except HTTPError as http_err:
            print(repr(http_err))
            print(f'Hubo un error en la petición: {http_err}')
    
    def tratar_respuesta(self):
        if(self.formatoRespuesta == "json"):
            self.datosRespuesta = self.respuesta.json()
         
    def realizar_peticion_api(self):
        try:
            self.crear_cabecera()
            self.transformar_datos_envio()    
            self.realizar_peticion()
            self.tratar_respuesta()
        except Exception as err:
            self.codigoRespuesta = 500
            print(repr)
            print(f'Ocurrió un error: {err}')
    
    def es_respuesta_correcta(self):
        return self.codigoRespuesta == 200
    
    def es_error_validacion_datos(self):
        return self.codigoRespuesta == 400
    
    def incluir_errores_formulario(self,formulario):
        errores = self.datosRespuesta
        for error in errores:
                formulario.add_error(error,errores[error])