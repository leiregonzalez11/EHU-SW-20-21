import signal
import sys
import psutil
import requests
import urllib
import json
from signal import SIGINT

import time

def clienteIoT():

    while True:
        #Obtención de los porcentajes de CPU y Ram
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        print("CPU: %" + str(cpu) + "\tRAM: %" + str(ram))

        #Subida/Actualización de datos en el canal
        uploadData(cpu,ram)

        time.sleep(15)

def handler(sig_num,frame):

    #Gestionar Evento
    print('\nSignal handler called with signal ' + str(SIGINT))
    print('\nCleaning channel...')
    clearChannel()
    print('\nExiting gracefully')
    sys.exit(0)

def channelCreator():

        metodo = 'POST'
        uri = "https://api.thingspeak.com/channels.json"
        cabeceras =  {'Host': 'api.thingspeak.com', 'Content-Type': 'application/x-www-form-urlencoded'}
        contenido = {'api_key': user_api_key, 'name': 'Mi Canal', 'field1': "%CPU", 'field2': "%RAM"}
        contenido_encoded = urllib.parse.urlencode(contenido)
        cabeceras['Content-Length'] = str(len(contenido_encoded))
        respuesta = requests.request(metodo, uri, data=contenido_encoded, headers=cabeceras, allow_redirects=False)
        codigo = respuesta.status_code
        contenido = respuesta.content

        return (contenido)


def getChannelApiKey(contenido):

    jsondecoded = json.loads (contenido)
    for api_keys in jsondecoded ["api_keys"]:
       if api_keys ['write_flag'] == True:
          api_key = str (api_keys ['api_key'])

    return (api_key)

def getChannelID(contenido):

    jsondecoded = json.loads (contenido)
    return(str (jsondecoded ["id"]))

def getUserApiKey():

    return ('xxxxxxxxxxxxxx') #User Api Key: Got it on ThingSpeak

def uploadData(cpu,ram):

    metodo = 'POST'
    uri = "https://api.thingspeak.com/update.json"
    field1 = str(cpu)
    field2 = str(ram)
    cabeceras = {'Host': 'api.thingspeak.com', 'Content-Type': 'application/x-www-form-urlencoded'}
    contenido = {'api_key': channel_api_key, 'field1': field1, 'field2': field2}
    contenido_encoded = urllib.parse.urlencode (contenido)
    cabeceras ['Content-Length'] = str (len (contenido_encoded))
    respuesta = requests.request (metodo, uri, data=contenido_encoded, headers=cabeceras, allow_redirects=False)

def clearChannel():

    metodo = 'DELETE'
    uri = "https://api.thingspeak.com/channels/" + channel_id + "/feeds.json"
    cabeceras = {'Host': 'api.thingspeak.com', 'Content-Type': 'application/x-www-form-urlencoded'}
    contenido = {'api_key': user_api_key}
    contenido_encoded = urllib.parse.urlencode (contenido)
    cabeceras ['Content-Length'] = str (len (contenido_encoded))
    respuesta = requests.request (metodo, uri, data=contenido_encoded, headers=cabeceras, allow_redirects=False)
    if (respuesta.status_code == 200):
        print ("--> Channel cleaned")
    else:
        print("Cannot clean channel " + channel_id)

def numChannels(respuesta):

    numchannels = 0
    contenido = respuesta.content
    jsondecoded = json.loads (contenido)

    for id in jsondecoded:
        numchannels = numchannels + 1;

    return (numchannels)

def channelExists(respuesta):

    exists = False;
    pass

def getChannels():

    metodo = 'GET'
    uri = "https://api.thingspeak.com/channels.json"
    cabeceras = {'Host': 'api.thingspeak.com', 'Content-Type': 'application/x-www-form-urlencoded'}
    contenido = {'api_key': user_api_key}
    contenido_encoded = urllib.parse.urlencode (contenido)
    cabeceras ['Content-Length'] = str (len (contenido_encoded))
    respuesta = requests.request (metodo, uri, data=contenido_encoded, headers=cabeceras, allow_redirects=False)
    contenido = respuesta.content

    return contenido


if __name__ == "__main__":

    user_api_key = getUserApiKey ()

    contenido = channelCreator()
    channel_api_key = getChannelApiKey (contenido)
    channel_id = getChannelID (contenido)

    print('Running. Press CTRL-C to exit. ')
    signal.signal (signal.SIGINT, handler)

    clienteIoT()


