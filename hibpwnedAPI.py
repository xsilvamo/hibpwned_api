#!/usr/bin/python3
from requests import RequestException
import hashlib
import requests
import json

#Declaramos los parametros indicados
api_key = 'aqui_tu_api_key' #Debes ingresar tu api key. Visita https://haveibeenpwned.com/api/ para obtener tu key.
api_option = 'breachedaccount/' #Esta es la opción que usaremos de la api

#Declaramos la url del webservice de la API
URL = 'https://haveibeenpwned.com/api/v3/'

#Creamos la clase de nuestro programa
class pwner:

    #Definimos el método inicializador
    def __init__(self, account, agent, key):
        self.account = account
        self.agent = agent
        self.key = key
        self.header = {'User-Agent': self.agent, "hibp-api-key": self.key}

    #Definimos nuestra función y nuestra petición
    def searchAllBreaches(self, truncate=False, domain=None, unverified=False):
    #Al cambiar el parámetro de truncate a True, nos parseará solo el nombre como información relevante

        #Definimos nuestra url de la petición
        url = URL + api_option
        if truncate == True:
            truncate = ''
        else:
            truncate = '?truncateResponse=false'
        if domain == None:
            domain = ''
        else:
            domain = '?domain=' + domain
        if unverified == True:
            unverified = '?includeUnverified=true'
        else:
            unverified = ''
        resp = requests.get(url + self.account + truncate + domain
                            + unverified, headers=self.header)
        self.checker(resp)
        if resp.status_code == 200:
            data = resp.json()
            return data
        else:
            return resp.status_code

    # Aqui se checkean los errores.
    def checker(self, resp):

        try:
            if resp.status_code == 400:
                print("400 - Solicitud incorrecta: La cuenta no cumple con un formato aceptable (es una cadena vacia)")
            elif resp.status_code == 401:
                print("No autorizado")
            elif resp.status_code == 403:
                print("403 - Prohibido - No se ha especificado ningun agente de usuario en la solicitud")
            elif resp.status_code == 404:
                print("404 - No encontrado - La cuenta no se pudo encontrar")
            elif resp.status_code == 429:
                print("Limite de velocidad excedido - Espere un momento para reintentar\n")
                print(resp.text)

        except RequestException:
            print("ERROR: Imposible conectar con el servidor")


correo = input("Ingresa el correo que quieres verificar: ")

#Le pasamos los parametros del inicializador
info = pwner(correo, 'app', api_key)
data = info.searchAllBreaches()
print(data)