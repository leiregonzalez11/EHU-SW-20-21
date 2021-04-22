import sys
import urllib

import requests
from bs4 import BeautifulSoup


def egelaSession():

    #Primera peticion

    print("Primera peticion \n")

    metodo = 'POST'
    uri =  'https://egela.ehu.eus/login/index.php'
    print ('Metodo: ' + metodo)
    print ('Uri: ' + uri + '\n')
    cabeceras = {'Host': uri.split('/')[2],
                 'Content-Type': 'application/x-www-form-urlencoded', }
    data = {'username': sys.argv[1],
            'password': sys.argv[2],}
    data_encoded = urllib.parse.urlencode (data)
    cabeceras ['Content-Length'] = str (len (data_encoded))
    respuesta = requests.request (metodo, uri, headers=cabeceras, data=data_encoded, allow_redirects=False)

    codigo = respuesta.status_code
    descripcion = respuesta.reason

    print (str (codigo) + " " + descripcion)

    for cabecera in respuesta.headers:
        print (cabecera + ": " + respuesta.headers [cabecera])

    print("")

    return (respuesta)


def getCookie (respuesta):
    cookie = respuesta.headers ['Set-Cookie'].split (',') [0]
    return (cookie)


def redirections(respuesta,cookie):

    print ("Primera redireccion \n")

    metodo = 'GET'
    uri = respuesta.headers ['Location']
    print ('Metodo: ' + metodo)
    print ('Uri: ' + uri + '\n')
    cookie = cookie
    cabeceras = {'Host': uri.split ('/') [2],
                 'Cookie': cookie}
    data = ''
    data_encoded = urllib.parse.urlencode (data)
    cabeceras ['Content-Length'] = str (len (data_encoded))
    respuesta = requests.request (metodo, uri, headers=cabeceras, data=data_encoded, allow_redirects=False)

    codigo = respuesta.status_code
    descripcion = respuesta.reason

    print (str (codigo) + " " + descripcion)

    for cabecera in respuesta.headers:
        print (cabecera + ": " + respuesta.headers [cabecera])

    print ("")

    print ("Segunda redireccion \n")

    metodo = 'GET'
    uri = respuesta.headers ['Location']
    print ('Metodo: ' + metodo)
    print ('Uri: ' + uri + '\n')
    cabeceras = {'Host': uri.split ('/') [2],
                 'Cookie': cookie}
    data = ''
    data_encoded = urllib.parse.urlencode (data)
    cabeceras ['Content-Length'] = str (len (data_encoded))
    respuesta = requests.request (metodo, uri, headers=cabeceras, data=data_encoded, allow_redirects=False)

    codigo = respuesta.status_code
    descripcion = respuesta.reason
    contenido = respuesta.content

    print (str (codigo) + " " + descripcion)

    for cabecera in respuesta.headers:
        print (cabecera + ": " + respuesta.headers [cabecera])

    print ("")

    return (respuesta)

def getUri(respuesta):

    soup = BeautifulSoup(respuesta.content,'html.parser')
    links = soup.find_all('a')
    i=0
    for link in links:
        if ('Sistemas Web' in link):
            print ("Link " + str(i) + ": " + str(link))
            uri = link.get('href')

    return (uri)

def downloadPDFs(uri,cookie):

    metodo = 'GET'
    uri = uri
    print ('Metodo: ' + metodo)
    print ('Uri: ' + uri + '\n')
    cabeceras = {'Host': uri.split ('/') [2],
                 'Cookie': cookie}
    data = ''
    data_encoded = urllib.parse.urlencode (data)
    cabeceras ['Content-Length'] = str (len (data_encoded))
    respuesta = requests.request (metodo, uri, headers=cabeceras, data=data_encoded, allow_redirects=False)

    codigo = respuesta.status_code
    descripcion = respuesta.reason
    contenido = respuesta.content

    print (str (codigo) + " " + descripcion)

    for cabecera in respuesta.headers:
        print (cabecera + ": " + respuesta.headers [cabecera])

    print ("")

    soup = BeautifulSoup(contenido, 'html.parser')
    links = soup.find_all('a')
    i = 0
    filelink = ''

    for link in links:
        imgs = link.find_all('img')
        for img in imgs:
            if ('pdf' in img['src']):
                filelink = link.get('href')
                print("Downloading file " + str(filelink.split('/')[5]).split('?')[1])
                print("Link " + str(i) + ": " + filelink)
                response = getPDF(filelink,cookie)
                print ("File downloaded")
                pdfname = response.headers['Content-Disposition'].split(';')[1].split('"')[1].split('.')[0]
                pdf = open(pdfname + ".pdf", 'wb')
                pdf.write(response.content)
                pdf.close()
                i = i + 1

def getPDF(filelink,cookie):

    metodo = 'GET'
    uri = filelink
    print ('Metodo: ' + metodo)
    print ('Uri: ' + uri + '\n')
    cabeceras = {'Host': uri.split ('/') [2], 'Cookie': cookie}
    data = ''
    data_encoded = urllib.parse.urlencode (data)
    cabeceras ['Content-Length'] = str (len (data_encoded))
    respuesta = requests.request (metodo, uri, headers=cabeceras, data=data_encoded, allow_redirects=False)

    codigo = respuesta.status_code
    descripcion = respuesta.reason

    print (str (codigo) + " " + descripcion)

    for cabecera in respuesta.headers:
        print (cabecera + ": " + respuesta.headers [cabecera])

    print ("")

    metodo = 'GET'
    uri = respuesta.headers ['Location']
    print ('Metodo: ' + metodo)
    print ('Uri: ' + uri + '\n')
    cabeceras = {'Host': uri.split ('/') [2], 'Cookie': cookie}
    data = ''
    data_encoded = urllib.parse.urlencode (data)
    cabeceras ['Content-Length'] = str (len (data_encoded))
    respuesta = requests.request (metodo, uri, headers=cabeceras, data=data_encoded, allow_redirects=False)

    codigo = respuesta.status_code
    descripcion = respuesta.reason
    contenido = respuesta.content

    print (str (codigo) + " " + descripcion)

    for cabecera in respuesta.headers:
        print (cabecera + ": " + respuesta.headers [cabecera])

    print ("")

    return (respuesta)


if  __name__ == '__main__':

    #Primero iniciamos sesión en egela:

    response = egelaSession()
    cookie = getCookie(response)
    respuesta = redirections(response,cookie)

    #Obtenemos la uri de la asignatura SISTEMAS WEB

    uri = getUri(respuesta)

    #Una vez obtenida la cookie e iniciada la sesión procedemos a descargar los pdfs:

    downloadPDFs(uri,cookie)