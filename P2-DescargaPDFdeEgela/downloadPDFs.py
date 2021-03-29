import urllib

import requests

def egelaSession():

    #Primera peticion

    print("Primera peticion \n")

    metodo = 'POST'
    uri =  'https://egela.ehu.eus/login/index.php'
    print ('Metodo: ' + metodo)
    print ('Uri: ' + uri + '\n')
    cabeceras = {'Host': uri.split('/')[2],
                 'Content-Type': 'application/x-www-form-urlencoded', }
    data = {'username': 'XXXXXX',
            'password': 'XXXXXXX',}
    data_encoded = urllib.parse.urlencode (data)
    cabeceras ['Content-Length'] = str (len (data_encoded))
    respuesta = requests.request (metodo, uri, headers=cabeceras, data=data_encoded, allow_redirects=False)

    codigo = respuesta.status_code
    descripcion = respuesta.reason

    print (str (codigo) + " " + descripcion)

    for cabecera in respuesta.headers:
        print (cabecera + ": " + respuesta.headers [cabecera])

    print("")

    print("Primera redireccion \n")

    metodo = 'GET'
    uri = respuesta.headers['Location']
    print ('Metodo: ' + metodo)
    print ('Uri: ' + uri + '\n')
    cookie = respuesta.headers['Set-Cookie'].split(',')[0]
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

    print("")


    print("Segunda redireccion \n")

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

    print("")

    print (contenido)
    print ("")

    print('Última petición: solicitar la página de Sistemas Web \n')

    #TODO: Obtener la uri del curso de la respuesta anterior

    metodo = 'GET'
    uri = 'https://egela.ehu.eus/course/view.php?id=43994'
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

    return (contenido)

def downloadPDFs(content):

    pass

if  __name__ == '__main__':

    content = egelaSession()
    downloadPDFs(content)