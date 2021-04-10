# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# <FirstCodeSnippet>
import os

from requests_oauthlib import OAuth2Session

import xlrd

graph_url = 'https://graph.microsoft.com/v1.0'


def get_user(token):
    graph_client = OAuth2Session(token=token)
    # Send GET to /me
    user = graph_client.get('{0}/me'.format(graph_url))

    # Return the JSON result
    return user.json()


# </FirstCodeSnippet>

# <GetCalendarSnippet>
def get_calendar_events(token):
    graph_client = OAuth2Session(token=token)

    # Configure query parameters to
    # modify the results
    query_params = {
        '$select': 'subject,organizer,start,end',
        '$orderby': 'createdDateTime DESC'
    }

    # Send GET to /me/events
    events = graph_client.get('{0}/me/events'.format(graph_url), params=query_params)
    print(events.json())
    # Return the JSON result
    return events.json()


# </GetCalendarSnippet>

# <GetFilesSnippet>
def get_user_files(token):
    graph_client = OAuth2Session(token=token)

    # Configure query parameters to
    # modify the results

    query_params = {
        '$select': 'name,createdBy,user'
    }

    # Send GET to /me/drive/root/children
    files = graph_client.get('{0}/me/drive/root/children'.format(graph_url), params=query_params)

    print(files.json())
    # Return the JSON result
    return files.json()


# </GetFilesSnippet>

def get_paths_to_upload(token,username):

    graph_client = OAuth2Session(token=token)
    root = graph_client.get('{0}/me/drive/root:/Documentos/Curso 2020-2021/TFM Activos:/children'.format(graph_url))

    for folder in root.json()['value']:

        if folder['name'].find(username) != -1:
            print("CARPETA--->", folder['name'])
            path_memoir = '/me/drive/root:/Documentos/Curso 2020-2021/TFM Activos/{0}/Memoria/'.format(folder['name'])
            path_documentation = '/me/drive/root:/Documentos/Curso 2020-2021/TFM Activos/{0}/Documentacion/'.format(folder['name'])
            path_sourcecode = '/me/drive/root:/Documentos/Curso 2020-2021/TFM Activos/{0}/Codigo Fuente/'.format(folder['name'])

    return path_memoir, path_sourcecode, path_documentation



# <GetFilesSnippet>
def get_user_shared_files(token):
    graph_client = OAuth2Session(token=token)



    # Configure query parameters to
    # modify the results

    # Send GET to /me/drive/root/children
    files = graph_client.get('{0}/me/drive/sharedWithMe'.format(graph_url))

    shared = graph_client.get('{0}/drives/33A0E52B21AB1E6D/items/33A0E52B21AB1E6D!109/children'.format(graph_url))

    root = graph_client.get('{0}/me/drive/root:/Documentos/Curso 2020-2021/TFM Activos:/children'.format(graph_url))

    final = graph_client.get('{0}/drives/d29cf38fb7d76d82/items/D29CF38FB7D76D82!137/children'.format(graph_url))

    '''/ drives / {remoteItem - driveId} / items / {remoteItem - id}'''

    print("--------------------------------------------------")

    #print("Drive id: " + files.json()['value'][0]['remoteItem']['parentReference']['driveId'])

   #print("Remote item id: " + files.json()['value'][0]['remoteItem']['id'])
    #print(files.json())
    ''' print("----------------AQUI VA EL SHARED----------------------------------")
    print(shared.json()['value'])
    person = "1.0"
    id_user = get_folder_id_user(token, person)

    print("El id de la carpeta del usuario es: ", id_user)
    id_sourcecode, id_documentation, id_memoir = get_children_folder_ids(token, id_user)
    print("El id de la carpeta de codigo fuente del usuario es: ", id_sourcecode)
    print("El id de la carpeta de documentacion del usuario es: ", id_documentation)
    print("El id de la carpeta de memoria del usuario es: ", id_memoir)

    print("-----------------AQUI VA EL ROOTS-------------------")
    print(root.json())
    print("Drive id de Documentos: " + root.json()['parentReference']['driveId'])
    print("Remote item id Documentos: " + root.json()['parentReference']['id'])'''

    print("----------------Muestrame que tienes-------------")
    print(root.json())
    cadena = "1.0"

    for folder in root.json()['value']:

            if folder['name'].find(cadena) != -1:
                print("CARPETA--->", folder['name'])

                print("CARPETA DRIVE ID----->",folder['parentReference']['driveId'])
                print("CARPETA remote item id----->", folder['parentReference']['id'])
                drive_id = folder['parentReference']['driveId']
                remote_item_id = folder['parentReference']['id']

    camino_memoria, camino_documentacion, camino_codigo = get_paths_to_upload(token)
    print("El camino para la memoria es: ", camino_memoria)
    print("El camino para la documentacion es: ", camino_documentacion)
    print("El camino para el codigo es: ", camino_codigo)

    #final2 = graph_client.get('{0}/drives/{1}/items/{2}/children'.format(graph_url,drive_id,remote_item_id))









    # Return the JSON result
    return files.json()
# </GetFilesSnippet>




