# -*- coding: UTF-8 -*-
from tkinter import messagebox
import requests
import urllib
from bs4 import BeautifulSoup
import time
import helper

class eGela:

    _login = 0
    _cookie = ""
    _refs = []
    _root = None

    def __init__(self, root):
        self._root = root

    def check_credentials(self, username, password, event=None):

        popup, progress_var, progress_bar = helper.progress("check_credentials", "Logging into eGela...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        #-------------------------------------------------------------

        print("##### 1. PETICION #####")
        metodo = 'POST'
        uri = "https://egela.ehu.eus/login/index.php"

        cabeceras = {'Host': uri.split ('/') [2],
                     'Content-Type': 'application/x-www-form-urlencoded', }

        data = {'username': username.get(),
                'password': password.get(), }

        data_encoded = urllib.parse.urlencode (data)
        cabeceras ['Content-Length'] = str (len (data_encoded))
        respuesta = requests.request (metodo, uri, headers=cabeceras, data=data_encoded, allow_redirects=False)

        codigo = respuesta.status_code
        descripcion = respuesta.reason

        print (str (codigo) + " " + descripcion)

        for cabecera in respuesta.headers:
            print (cabecera + ": " + respuesta.headers [cabecera])

        print ("")


        progress = 33
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(1)

        #------------------------------------------------------------------------

        print("\n##### 2. PETICION #####")

        metodo = 'GET'
        uri = respuesta.headers ['Location']
        print ('Metodo: ' + metodo)
        print ('Uri: ' + uri + '\n')
        cookie = respuesta.headers ['Set-Cookie'].split (',') [0]
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

        progress = 66
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(1)

        #-------------------------------------------------------------------

        print("\n##### 3. PETICION #####")


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

        progress = 100
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(1)
        popup.destroy()

        if codigo==200:

            self._login = 1
            self._cookie = cookie
            self._root.destroy()
            print("Login correct!")

        else:
            messagebox.showinfo("Alert Message", "Login incorrect!")


    def get_pdf_refs(self):

        popup, progress_var, progress_bar = helper.progress("get_pdf_refs", "Downloading PDF list...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("\n##### 4. PETICION (Página principal de la asignatura en eGela) #####")


        metodo = 'GET'
        uri = 'https://egela.ehu.eus/course/view.php?id=43994'
        print ('Metodo: ' + metodo)
        print ('Uri: ' + uri + '\n')
        cabeceras = {'Host': uri.split ('/') [2],
                     'Cookie': self._cookie}
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


        print("\n##### Analisis del HTML... #####")


        soup = BeautifulSoup (contenido, 'html.parser')

        links = soup.find_all ('a')

        progress_step = float (100.0 / len (links))

        filelink = ''
        self._refs =[]

        for link in links:
            imgs = link.find_all ('img')
            for img in imgs:
                if ('pdf' in img ['src']):
                    filelink = link.get ('href')
                    pdf_name = link.span.text

                    self._refs.append({'pdf_name': pdf_name , 'pdf_link': filelink})

                    progress += progress_step
                    progress_var.set(progress)
                    progress_bar.update()
                    time.sleep(0.1)


        popup.destroy()
        return self._refs


    def get_pdf(self, selection):

        print("\t##### descargando  PDF... #####")

        metodo = 'GET'
        uri = self._refs[selection]['pdf_link']
        print ('Metodo: ' + metodo)
        print ('Uri: ' + uri + '\n')
        cabeceras = {'Host': uri.split ('/') [2], 'Cookie': self._cookie}
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

        metodo = 'GET'
        uri = respuesta.headers ['Location']
        print ('Metodo: ' + metodo)
        print ('Uri: ' + uri + '\n')
        cabeceras = {'Host': uri.split ('/') [2], 'Cookie': self._cookie}
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

        pdf_name = self._refs[selection]['pdf_name']
        pdf_content = respuesta.content

        print ("File " + pdf_name + " downloaded")


        return pdf_name, pdf_content

