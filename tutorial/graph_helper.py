# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# <FirstCodeSnippet>

from datetime import date
import json
from tutorial.models import Bibliografia
import json
import os

from pip._vendor.webencodings import Encoding
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

    '''query_params = {
        '$select': 'name,createdBy,user'
    }

    # Send GET to /me/drive/root/children
    files = graph_client.get('{0}/me/drive/root/children'.format(graph_url), params=query_params)'''

    query_params = {
        '$select': 'name,parentReference,id'
    }
    files = graph_client.get('{0}/me/drive/root:/Documentos/Curso 2020-2021/TFM Activos:/children'.format(graph_url),params=query_params)

    print(files.json())

    ''' x = '{ "dni":"John", "name":30, "folder":"New York"}'
    files2 = json.loads(x)
    print("----------------------",type(files2))
    print("------------INFORMACION-------------")

    for user in files.json()['value']:
        files2['dni'] = user['name'].split('-')[1]
        files2['name'] = user['name'].split('-')[0]
        files2['folder'] = user['folder']

    for l in files2.values():
        print(l)'''

        # Return the JSON result
    return files.json()


# </GetFilesSnippet>

def get_paths_to_upload(token, username):
    graph_client = OAuth2Session(token=token)
    root = graph_client.get('{0}/me/drive/root:/Documentos/Curso 2020-2021/TFM Activos:/children'.format(graph_url))

    for folder in root.json()['value']:

        if folder['name'].find(username) != -1:
            print("CARPETA--->", folder['name'])
            path_memoir = '/me/drive/root:/Documentos/Curso 2020-2021/TFM Activos/{0}/Memoria/'.format(folder['name'])
            path_memoir_content = '/me/drive/root:/Documentos/Curso 2020-2021/TFM Activos/{0}/Memoria:/content'.format(folder['name'])
            path_documentation = '/me/drive/root:/Documentos/Curso 2020-2021/TFM Activos/{0}/Documentacion/'.format(
                folder['name'])
            path_sourcecode = '/me/drive/root:/Documentos/Curso 2020-2021/TFM Activos/{0}/Codigo Fuente/'.format(
                folder['name'])

    return path_memoir_content, path_memoir, path_sourcecode, path_documentation


def create_folder(token):
    graph_client = OAuth2Session(token=token)
    result = graph_client.post('{0}/me/drive/root/children'.format(graph_url))

    return result


# <GetFilesSnippet>
def get_user_shared_files(token):
    graph_client = OAuth2Session(token=token)

    # Configure query parameters to
    # modify the results

    # Send GET to /me/drive/root/children
    files = graph_client.get('{0}/me/drive/sharedWithMe'.format(graph_url))

    shared = graph_client.get('{0}/drives/33A0E52B21AB1E6D/items/33A0E52B21AB1E6D!109/children'.format(graph_url))

    query_params = {
        '$select': 'name,parentReference,folder'
    }

    root = graph_client.get('{0}/me/drive/root:/Documentos/Curso 2020-2021/TFM Activos:/children'.format(graph_url))

    final = graph_client.get('{0}/drives/d29cf38fb7d76d82/items/D29CF38FB7D76D82!137/children'.format(graph_url))

    carpetaleida = graph_client.get('{0}/me/drive/root:/Documentos/Curso 2020-2021:/children'.format(graph_url))

    for folder in carpetaleida.json()['value']:
        if folder['name'] == 'TFM Leidos':
            id = folder['id']
            print("EL ID ES:", id)

    for user in root.json()['value']:

        patch = graph_client.patch('{0}/me/drive/items/{1}'.format(graph_url, user['id']),
                                   headers={'Content-Type': 'application/json'},
                                   json={
                                       "parentReference": {
                                           "id": id
                                       },
                                       "name": user['name']
                                   })





    id_folder = Bibliografia.objects.filter(author='Iván Abalde Costas')

    path = id_folder[0].id_folder








    print("-------------Informacion sobre root creada ------------------")
    #print(OAuth2Session(token='https://graph.microsoft.com/v1.0/me/drive/root:/Documentos/Curso 2020-2021/TFM Activos/Abalde Costas Iván-1.0/Memoria/ExcedenciaArbitral.pdf:/content'))
    print(root.json()['value'][1])





    ''' data_set = {"name": "New Folder", "folder": {} , "@microsoft.graph.conflictBehavior": "rename"}

    json_dump = json.dumps(data_set)

    json_object = json.loads(json_dump)

    print(json_object)
    '''
    '''
    result = graph_client.post('{0}/me/drive/items/D29CF38FB7D76D82!104/children'.format(graph_url),
                               headers={'Authorization': 'Bearer ' + str(token),
                                        'Content-Type': 'application/json'},
                               json={
                                   "name": "Nuevo Curso 1",
                                   "folder": {},
                                   "@microsoft.graph.conflictBehavior": "rename"
                               })

    print("-------------Información sobre la respuesta ------------------")

    print(result)
    print(result.json())

    print("-----------------AQUI VA EL ROOTS-------------------")
    print(root.json())

    # folder = create_folder(token)

    
    '''
    print("--------------------------------------------------")

    # print("Drive id: " + files.json()['value'][0]['remoteItem']['parentReference']['driveId'])

    # print("Remote item id: " + files.json()['value'][0]['remoteItem']['id'])
    # print(files.json())
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
    print("Remote item id Documentos: " + root.json()['parentReference']['id'])

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
    '''

    # print(folder.json())

    # Return the JSON result
    return files.json()


# </GetFilesSnippet>

def list_all_user_folders():
    print("---------------------VA A LEER ARCHIVO DE ALUMNOS-----------------------------")

    openFile = xlrd.open_workbook("D:\\TFG - Repositorio TFM\\Repositorio TFM\\tutorial\\AlumnosMatriculadosTFG.xlsx")
    sheet = openFile.sheet_by_name("Alumnado_20_21")

    userList = []
    contador = 0
    while contador <= 10 :
            if str(sheet.cell_value(contador, 1)) != "Alumno" and sheet.cell_value(contador, 1) != "administrador":
                userList.append(str(sheet.cell_value(contador, 1)).replace(',', '') + "-" + str(sheet.cell_value(contador, 0)))
            contador = contador + 1

    return userList



def create_academic_course(token):

    today = date.today()


    actual_year = today.strftime("%Y")

    last_year = int(actual_year)-1

    course_year = "Curso " + str(last_year) + "-" + actual_year

    graph_client = OAuth2Session(token=token)

    list = [course_year, 'TFM Activos', 'TFM Leidos']

    result = graph_client.post('{0}/me/drive/items/D29CF38FB7D76D82!104/children'.format(graph_url),
                               headers={'Authorization': 'Bearer ' + str(token),
                                        'Content-Type': 'application/json'},
                               json={
                                   "name": list.pop(0),
                                   "folder": {},
                                   "@microsoft.graph.conflictBehavior": "rename"
                               })
    print("-------------------El Resultado es este--------------------")
    print(result.json()['id'])
    dict = { course_year : result.json()['id']}
    listUserFolder = ['Memoria', 'Documentacion', 'Codigo Fuente', 'Actas']

    for l in list:

          nextresult = graph_client.post('{0}/me/drive/items/{1}/children'.format(graph_url,result.json()['id']),
                                   headers={'Authorization': 'Bearer ' + str(token),
                                            'Content-Type': 'application/json'},
                                   json={
                                       "name": l,
                                       "folder": {},
                                       "@microsoft.graph.conflictBehavior": "rename"
                                   })
          dict[l] = nextresult.json()['id']


    userlist = list_all_user_folders()

    for l in userlist:
        user = graph_client.post('{0}/me/drive/items/{1}/children'.format(graph_url,dict['TFM Activos']),
                         headers={'Authorization': 'Bearer ' + str(token),
                                  'Content-Type': 'application/json'},
                         json={
                             "name": l,
                             "folder": {},
                             "@microsoft.graph.conflictBehavior": "rename"
                         })
        dict[l] = user.json()['id']


        for i in listUserFolder:
            graph_client.post('{0}/me/drive/items/{1}/children'.format(graph_url, user.json()['id']),
                              headers={'Authorization': 'Bearer ' + str(token),
                                       'Content-Type': 'application/json'},
                              json={
                                  "name": i,
                                  "folder": {},
                                  "@microsoft.graph.conflictBehavior": "rename"
                              })
    '''for i in dict:
        print(i, dict[i])'''


    return result.json()

def get_read_id_folder(token):
    graph_client = OAuth2Session(token=token)

    readfolderid = graph_client.get('{0}/me/drive/root:/Documentos/Curso 2020-2021:/children'.format(graph_url))

    for folder in readfolderid.json()['value']:
        if folder['name'] == 'TFM Leidos':
            id = folder['id']

    return id;

def move_single_folder_to_read(token, id, name):

    graph_client = OAuth2Session(token=token)

    parentReference_id = get_read_id_folder(token)

    patch = graph_client.patch('{0}/me/drive/items/{1}'.format(graph_url, id),
                                   headers={'Content-Type': 'application/json'},
                                   json={
                                       "parentReference": {
                                           "id": parentReference_id
                                       },
                                       "name": name
                                   })

    return patch.json()


