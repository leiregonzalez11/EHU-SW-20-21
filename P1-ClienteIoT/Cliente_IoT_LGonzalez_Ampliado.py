import signal
import sys
from datetime import datetime
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
    print('\nSignal handler called with signal ' + str(SIGINT) + "\n")
    print ('Getting information about the channel to a file...')
    writeToFile(path)
    print('\nCleaning channel...')
    clearChannel()
    print('\nExiting gracefully')
    sys.exit(0)

def channelCreator():

        metodo = 'POST'
        uri = "https://api.thingspeak.com/channels.json"
        cabeceras =  {'Host': 'api.thingspeak.com', 'Content-Type': 'application/x-www-form-urlencoded'}
        contenido = {'api_key': user_api_key, 'name': channelName, 'field1': "%CPU", 'field2': "%RAM"}
        contenido_encoded = urllib.parse.urlencode(contenido)
        cabeceras['Content-Length'] = str(len(contenido_encoded))
        respuesta = requests.request(metodo, uri, data=contenido_encoded, headers=cabeceras, allow_redirects=False)
        codigo = respuesta.status_code
        contenido = respuesta.content

        return (contenido)

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
    uri = "https://api.thingspeak.com/channels/" + str(channel_id) + "/feeds.json"
    cabeceras = {'Host': 'api.thingspeak.com', 'Content-Type': 'application/x-www-form-urlencoded'}
    contenido = {'api_key': user_api_key}
    contenido_encoded = urllib.parse.urlencode (contenido)
    cabeceras ['Content-Length'] = str (len (contenido_encoded))
    respuesta = requests.request (metodo, uri, data=contenido_encoded, headers=cabeceras, allow_redirects=False)
    if (respuesta.status_code == 200):
        print ("--> Channel cleaned")
    else:
        print("Cannot clean channel " + channel_id)

def getChannelApiKey(contenido):

    jsondecoded = json.loads (contenido)
    if channelExists():
        for channel in jsondecoded:
            if channel ['name'] == channelName:
                for apikeys in channel ['api_keys']:
                    if apikeys ['write_flag'] == True:
                        api_key = str (apikeys ['api_key'])

    else:
        for api_keys in jsondecoded ["api_keys"]:
           if api_keys ['write_flag'] == True:
              api_key = str (api_keys ['api_key'])

    return (api_key)

def getChannelID(contenido):

    jsondecoded = json.loads (contenido)
    if channelExists():
        for names in jsondecoded:
            if names ['name'] == channelName:
                channelId = names ['id']
    else:
        channelId = str (jsondecoded ["id"])

    return(channelId)

def getUserApiKey():

    return ('xxxxxxxxxxxx') #User Api Key: Got it on your ThingSpeak

#Funciones incluídas para la ampliación de la práctica

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

def numChannels(contenido):

    numchannels = 0
    jsondecoded = json.loads(contenido)

    for id in jsondecoded:
        numchannels = numchannels + 1;

    return (numchannels)

def channelExists():

    exists = False
    jsondecoded = json.loads (channels)

    for channel in jsondecoded:
        if channel ['name'] == channelName:
            exists = True
    return (exists)

def getChannelInfo():

    metodo = 'GET'
    uri = "https://api.thingspeak.com/channels/" + str(channel_id) + "/feeds.xml"
    cabeceras = {'Host': 'api.thingspeak.com', 'Content-Type': 'application/x-www-form-urlencoded'}
    contenido = {'api_key': channel_api_key}
    contenido_encoded = urllib.parse.urlencode (contenido)
    cabeceras ['Content-Length'] = str (len (contenido_encoded))
    respuesta = requests.request (metodo, uri, data=contenido_encoded, headers=cabeceras, allow_redirects=False)
    contenido = respuesta.content

    return (contenido)

def writeToFile(path):

    content = getChannelInfo()
    file = open(path, "w")
    file.write(str(datetime.now()) + "\n")
    file.write("Channel name: " + channelName + "\n")
    file.write(str(content))
    file.close()

if __name__ == "__main__":

    user_api_key = getUserApiKey()
    channelName = "Mi canal3"
    path = "../../../PycharmProjects/practica1sw/channelInfo.txt"

    channels = getChannels()

    if numChannels(channels) < 4 and not channelExists():

        print ("\n Creating new channel... \n")

        contenido = channelCreator()
        channel_api_key = getChannelApiKey(contenido)
        channel_id = getChannelID(contenido)

        print('Running. Press CTRL-C to exit. \n')
        signal.signal (signal.SIGINT, handler)

        clienteIoT()

    else:

        if channelExists():

            print ("\n Channel exists. Getting information about it... \n")

            channel_id = getChannelID(channels)
            channel_api_key = getChannelApiKey (channels)

            print ('Running. Press CTRL-C to exit. \n')
            signal.signal (signal.SIGINT, handler)

            clienteIoT ()

        else:
            print ("\n Cannot create more channels. Delete one channel to create a new one")