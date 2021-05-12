from wsgiref import headers

import requests
import urllib
import webbrowser
from socket import AF_INET, socket, SOCK_STREAM
import json
import helper

app_key = 'kfacoosqtm5n9zp'
app_secret = 'bgyqh2dt1xmpq6h'
server_addr = "localhost"
server_port = 8090
redirect_uri = "http://" + server_addr + ":" + str(server_port)

class Dropbox:
    _access_token = ""
    _path = "/"
    _files = []
    _root = None
    _msg_listbox = None

    def __init__(self, root):
        self._root = root


    def local_server(self):

        # 8090. portuan entzuten dagoen zerbitzaria sortu
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((server_addr, server_port))
        server_socket.listen(1)
        print("\tLocal server listening on port " + str(server_port))

        # nabitzailetik 302 eskaera jaso
        client_connection, client_address = server_socket.accept()
        eskaera = client_connection.recv(1024)
        print("\tRequest from the browser received at local server:")
        print (eskaera)


        # eskaeran "auth_code"-a bilatu
        # --> aquiii
        lehenengo_lerroa = eskaera.decode('UTF8').split('\n')[0]
        aux_auth_code = lehenengo_lerroa.split(' ')[1]
        auth_code = aux_auth_code[7:].split('&')[0]
        print ("\tauth_code: " + auth_code)

        # erabiltzaileari erantzun bat bueltatu
        http_response = "HTTP/1.1 200 OK\r\n\r\n" \
                        "<html>" \
                        "<head><title>Proba</title></head>" \
                        "<body>The authentication flow has completed. Close this window.</body>" \
                        "</html>"
        client_connection.sendall(http_response.encode(encoding="utf-8"))
        client_connection.close()
        server_socket.close()

        return auth_code

    def do_oauth(self):

        uri = "https://www.dropbox.com/oauth2/authorize"
        #cabeceras = {'Host': 'api.dropboxapi.com'}
        datos = {'response_type': 'code',
                 'client_id': app_key,
                 'redirect_uri': redirect_uri}

        datos_encoded = urllib.parse.urlencode(datos)

        print ("\tOpenning browser...")

        webbrowser.open_new_tab ((uri + '?' + datos_encoded))

        print ("# Step 4: Handle the OAuth 2.0 server response")

        #--> Falla aqui
        #auth_code = self.local_server()
        auth_code = Dropbox.local_server(self)

        print ("# Step 5: Exchange authorization code for refresh and access tokens")

        uri = 'https://api.dropboxapi.com/oauth2/token'

        cabeceras = {'Content-Type': 'application/x-www-form-urlencoded'}

        datos = {'code': auth_code,
                 'client_id': app_key,
                 'client_secret': app_secret,
                 'redirect_uri': redirect_uri,
                 'grant_type': 'authorization_code'}

        respuesta = requests.post (uri, headers=cabeceras, data=datos, allow_redirects=False)
        status = respuesta.status_code
        print ("\tStatus: " + str(status))

        contenido = respuesta.text
        print ("\tContenido:")
        print (contenido)
        contenido_json = json.loads (contenido)
        self._access_token = contenido_json ['access_token']
        print ("\taccess_token: " + self._access_token)

        self._root.destroy()

    def list_folder(self, msg_listbox):

        print("/list_folder")

        uri = 'https://api.dropboxapi.com/2/files/list_folder'
        # https://www.dropbox.com/developers/documentation/http/documentation#files-list_folder

        headers = {'Authorization': 'Bearer ' + self._access_token,
                   'Content-Type': 'application/json'}

        data = {"path": self._path if self._path != '/' else '',
                 "recursive": False,
                 "include_deleted": False,
                 "include_has_explicit_shared_members": False,
                 "include_mounted_folders": True,
                 "include_non_downloadable_files": True}

        datos_json = json.dumps(data)
        response = requests.post(uri, headers=headers, data=datos_json, allow_redirects=False)
        status = response.status_code
        print ("\tStatus: " + str (status))
        print (response.text)

        self._files = helper.update_listbox2 (msg_listbox, self._path, response.json())

    def transfer_file(self, file_path, file_data):

        print("/upload")

        uri = 'https://content.dropboxapi.com/2/files/upload'
        # https://www.dropbox.com/developers/documentation/http/documentation#files-upload

        headers = {'Authorization': 'Bearer ' + self._access_token,
                   'Content-Type': 'application/octet-stream'}

        data = {"path": file_path,
                 "mode": "add",
                 "autorename": True,
                 "mute": False,
                 "strict_conflict": False
                 }

        headers['Dropbox-API-Arg'] = json.dumps(data)
        response = requests.post (uri, headers=headers, data=file_data, allow_redirects=False)

        status = response.status_code
        print ("\tStatus: " + str (status))
        print (response.text)

    def delete_file(self, file_path):

        print("/delete_file")

        uri = 'https://api.dropboxapi.com/2/files/delete_v2'
        # https://www.dropbox.com/developers/documentation/http/documentation#files-delete

        uri = 'https://api.dropboxapi.com/2/files/delete_v2'

        headers = {'Authorization': 'Bearer ' + self._access_token,
                   'Content-Type': 'application/json'}

        data = {"path": file_path}
        json_data = json.dumps(data)

        response = requests.post (uri, headers=headers, data=json_data, allow_redirects=False)
        status = response.status_code
        print ("\tStatus: " + str (status))
        print (response.text)

    def create_folder(self, path):

        print("/create_folder")

        # https://www.dropbox.com/developers/documentation/http/documentation#files-create_folder

        uri = 'https://api.dropboxapi.com/2/files/create_folder_v2'

        headers = {'Authorization': 'Bearer ' + self._access_token,
                   'Content-Type': 'application/json'}

        data = {"path": path,
                "autorename": False}

        json_data = json.dumps (data)

        response = requests.post (uri, headers=headers, data=json_data, allow_redirects=False)
        status = response.status_code
        print ("\tStatus: " + str (status))
        print (response.text)



