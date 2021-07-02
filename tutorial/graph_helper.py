# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# <FirstCodeSnippet>

from datetime import date
import json

import yaml
import os

from django.http import HttpResponseRedirect
from xlrd import XLRDError
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail

from tutorial.models import Bibliografia, Profesor
import json
import os
import base64
from pip._vendor.webencodings import Encoding
from requests_oauthlib import OAuth2Session



'''from authlib.integrations.requests_client import OAuth2Session'''

stream = open('oauth_settings.yml', 'r')
settings = yaml.load(stream, yaml.SafeLoader)

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
    print("El token es: ", token)
    print("HASTA AQUI!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
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
    course_year = get_active_course_name()
    files = graph_client.get('{0}/me/drive/root:/Documentos/{1}/TFM Activos:/children'.format(graph_url,course_year),params=query_params)


    '''print("Va a empezar el nuevo diccionario")
    for folder in dict['value']:
        print("Alumno: ------------->", folder)'''


    #print(files.json())

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

# <GetFilesSnippet>
def get_user_files_readed(token):
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
    course_year = get_active_course_name()
    files = graph_client.get('{0}/me/drive/root:/Documentos/{1}/TFM Leidos:/children'.format(graph_url,course_year),params=query_params)

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
    course_year = get_active_course_name()
    root = graph_client.get('{0}/me/drive/root:/Documentos/{1}/TFM Activos:/children'.format(graph_url, course_year))


    for folder in root.json()['value']:

        if folder['name'].find(username) != -1:
            print("CARPETA--->", folder['name'])

            path_memoir = '/me/drive/root:/Documentos/{1}/TFM Activos/{0}/Memoria/'.format(folder['name'], course_year)
            path_memoir_content = '/me/drive/root:/Documentos/{1}/TFM Activos/{0}/Memoria:/content'.format(folder['name'], course_year)
            path_documentation = '/me/drive/root:/Documentos/{1}/TFM Activos/{0}/Documentacion/'.format(
                folder['name'], course_year)
            path_sourcecode = '/me/drive/root:/Documentos/{1}/TFM Activos/{0}/Codigo Fuente/'.format(
                folder['name'], course_year)



    return path_memoir_content, path_memoir, path_sourcecode, path_documentation


def create_folder(token):
    graph_client = OAuth2Session(token=token)
    result = graph_client.post('{0}/me/drive/root/children'.format(graph_url))

    return result


# <GetFilesSnippet>
def get_user_shared_files(token):
    graph_client = OAuth2Session(token=token)

    '''print("Graph Client-------->\n", graph_client)
    scope = settings['scopes']
    redirect_uri = settings['redirect']
    client_id = settings['app_id']
    client_secret = settings['app_secret']
    scope = 'user:email'
    scopes = settings['scopes']
    authorize_url = '{0}{1}'.format(settings['authority'], settings['authorize_endpoint'])
    token_url = '{0}{1}'.format(settings['authority'], settings['token_endpoint'])

    print("scope;", scopes)
    print("client id:", client_id)
    print("client_secret:", client_secret)
    graph = OAuth2Session(client_id, client_secret, scope=scope)
    print("Graph client 2------>\n", graph)
    #authorization_endpoint = 'https://login.microsoftonline.com/common'
    uri, state = graph.create_authorization_url(authorize_url)
    token = graph.fetch_token(token_url, user='jorgeruiztfg@hotmail.com', password='Paraeltfg777')

    print(token)
    print(token_url)
    print("URI:", uri)
    print("State:,",state)'''
    # using requests implementation
    #graph_client = OAuth2Session(client_id, client_secret, scope=scope)

    # Configure query parameters to
    # modify the results

    # Send GET to /me/drive/root/children
    files = graph_client.get('{0}/me/drive/sharedWithMe'.format(graph_url))


    '''bibliografia = Bibliografia(dni="44492748F", author="Jorge Ruíz Pérez", title="Repositorio TFMs",keyword="Repositorio, archivos, python",description="Es un repositorio que permite subir, consultar, administrar archivos académicos", memoir="file",id_folder="inventada", tutor="Rosalia Laza Fidalgo", cotutor="Reyes Pavón Ríal", readed=True)
    bibliografia2 = Bibliografia(dni="45678901Q", author="Miranda Sobrado Paula", title="Redes de Distribución",keyword="Redes, cables, cisco",
                                description="Aplicación de distribución de redes",
                                memoir="file", id_folder="inventada2", tutor="Silvana Gómez Meire",
                                cotutor="",readed=True)

    bibliografia.save()
    bibliografia2.save()
    print("BIBLIO---->", Bibliografia.objects.all())'''
    '''root = graph_client.get('{0}/me/drive/root:/Documentos:/children'.format(graph_url))
    today = date.today()

    actual_year = today.strftime("%Y")

    last_year = int(actual_year) - 1

    course_year = "Curso " + str(last_year) + "-" + actual_year


    for folder in root.json()['value']:
        if folder['name'] == course_year:
            print("El curso con la carpeta: " + str(folder['name']) + " ya ha sido creado" )
        else:
            print("El curso actual :" + str(folder['name']) + " aun no ha sido creado")'''




    '''shared = graph_client.get('{0}/drives/33A0E52B21AB1E6D/items/33A0E52B21AB1E6D!109/children'.format(graph_url))

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
'''




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

    print("---------------------VA A LEER ARCHIVO DE ALUMNOS-----------------------------")


    ''' router = get_all_courses_in_active(token)

    for route in router['value']:
        print("Nombre de la carpeta : " ,route['name'])'''




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

    actualpath = os.getcwd()
    print("Al leer el archivo de Alumnos el path es: ", actualpath)
    os.chdir(r'tutorial/static/config/')

    name = "Alumnado_"

    today = date.today()

    actual_year = today.strftime("%Y")[-2:]

    last_year = int(actual_year) - 1
    future_year = int(actual_year) + 1

    last_year = str(last_year)[-2:]
    future_year = str(future_year)[-2:]

    actual_course_name = name + actual_year + "_" + future_year
    # last_course_name = name + last_year + "_" + actual_year

    openFile = xlrd.open_workbook("AlumnosMatriculadosTFG.xls")

    #actual_course_sheet = openFile.sheet_by_name(actual_course_name)
    # last_course_sheet = openFile.sheet_by_name(last_course_name)

    sheet = openFile.sheet_by_name(actual_course_name)


    userList = []
    '''contador = 0
    while contador <= 10 :
            if str(sheet.cell_value(contador, 1)) != "Alumno" and sheet.cell_value(contador, 1) != "administrador":
                userList.append(str(sheet.cell_value(contador, 1)).replace(',', '') + "-" + str(sheet.cell_value(contador, 0)))
            contador = contador + 1
        '''

    for i in range(sheet.nrows):

        if str(sheet.cell_value(i, 1)) != "Alumno" and str(sheet.cell_value(i, 1)) != "administrador" and sheet.cell_value(i, 0):
                 userList.append(str(sheet.cell_value(i, 1)).replace(',', '') + "-" + str(sheet.cell_value(i, 0)))

    os.chdir(actualpath)
    print("El path al ACABAR la lectura de alumnos se encuentra en: ", os.getcwd())
    return userList


def get_user_tutors(user_dni):

    '''print(os.getcwd())
    os.chdir(r'tutorial/static/config/')'''

    actualpath = os.getcwd()
    print("El path al leer el archivo de TUTORES se encuentra en: ", actualpath)
    os.chdir(r'tutorial/static/config/')
    name = "Alumnado_"

    today = date.today()

    actual_year = today.strftime("%Y")[-2:]

    last_year = int(actual_year) - 1
    future_year = int(actual_year) + 1

    last_year = str(last_year)[-2:]
    future_year = str(future_year)[-2:]

    actual_course_name = name + actual_year + "_" + future_year
    # last_course_name = name + last_year + "_" + actual_year

    openFile = xlrd.open_workbook("AlumnosMatriculadosTFG.xls")

    # actual_course_sheet = openFile.sheet_by_name(actual_course_name)
    # last_course_sheet = openFile.sheet_by_name(last_course_name)

    sheet = openFile.sheet_by_name(actual_course_name)

    print("N. de filas", sheet.nrows)

    print("N de columnas", sheet.ncols)
    tutor = ""
    cotutor = ""

    for i in range(sheet.nrows):

        if str(sheet.cell_value(i, 0)) == user_dni:
            if str(sheet.cell_value(i, 3)) == "":
                print("No tiene tutor el usuario con dni:", user_dni)
            else:
                print("Se ha encontrado el tutor del alumno con DNI: " + user_dni + " y es " + str(
                    sheet.cell_value(i, 3)))
                tutor = str(
                    sheet.cell_value(i, 3))
            if str(sheet.cell_value(i, 4)) == "":
                print("No tiene co-tutor el usuario con DNI: ", user_dni)
            else:
                print("Se ha encontrado el cotutor del alumno con DNI: " + user_dni + " y es "+ str(sheet.cell_value(i, 4)))
                cotutor = str(sheet.cell_value(i, 4))

    os.chdir(actualpath)
    print("El path al ACABAR de leer el archivo de TUTORES se encuentra en: ", os.getcwd())
    return tutor, cotutor



def create_academic_course(token):

    course_year = get_active_course_name()

    graph_client = OAuth2Session(token=token)

    list = [course_year, 'TFM Activos', 'TFM Leidos']

    root = graph_client.get('{0}/me/drive/root:/Documentos:/children'.format(graph_url))



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

def get_read_id_folder(token, course=None):
    graph_client = OAuth2Session(token=token)
    course_year = get_active_course_name()

    if course is not None:
        course_year = course

    readfolderid = graph_client.get('{0}/me/drive/root:/Documentos/{1}:/children'.format(graph_url, course_year))

    for folder in readfolderid.json()['value']:
        if folder['name'] == 'TFM Leidos':
            id = folder['id']

    return id;

def get_active_id_folder(token):
    graph_client = OAuth2Session(token=token)
    course_year = get_active_course_name()
    activefolderid = graph_client.get('{0}/me/drive/root:/Documentos/{1}:/children'.format(graph_url,course_year))

    for folder in activefolderid.json()['value']:
        if folder['name'] == 'TFM Activos':
            id = folder['id']

    return id;

def move_single_folder_to_read(token, id, name, course=None):

    graph_client = OAuth2Session(token=token)

    if course is not None:
        parentReference_id = get_read_id_folder(token, course)
    else:
        parentReference_id = get_read_id_folder(token)

    patch = graph_client.patch('{0}/me/drive/items/{1}'.format(graph_url, id),
                                   headers={'Content-Type': 'application/json'},
                                   json={
                                       "parentReference": {
                                           "id": parentReference_id
                                       },
                                       "name": name
                                   })

    listUserFolder = ['Memoria', 'Documentacion', 'Codigo Fuente', 'Actas']

    return patch.json()

def create_user_folder_in_active(token, name):

    graph_client = OAuth2Session(token=token)

    id_folder = get_active_id_folder(token)

    listUserFolder = ['Memoria', 'Documentacion', 'Codigo Fuente', 'Actas']

    result = graph_client.post('{0}/me/drive/items/{1}/children'.format(graph_url, id_folder),
                               headers={'Authorization': 'Bearer ' + str(token),
                                        'Content-Type': 'application/json'},
                               json={
                                   "name": name,
                                   "folder": {},
                                   "@microsoft.graph.conflictBehavior": "rename"
                               })

    for l in listUserFolder:
       graph_client.post('{0}/me/drive/items/{1}/children'.format(graph_url, result.json()['id']),
                                       headers={'Authorization': 'Bearer ' + str(token),
                                                'Content-Type': 'application/json'},
                                       json={
                                           "name": l,
                                           "folder": {},
                                           "@microsoft.graph.conflictBehavior": "rename"
                                       })


    return result.json()


def get_dni_student_common():

    able = False
    '''print(os.getcwd())
    os.chdir(r'tutorial/static/config/')'''

    actualpath = os.getcwd()
    print("AL INICIAR la lectura de los dni en común el path es: ", actualpath)
    os.chdir(r'tutorial/static/config/')
    name = "Alumnado_"

    today = date.today()

    actual_year = today.strftime("%Y")[-2:]

    last_year = int(actual_year) - 1
    future_year = int(actual_year) + 1

    last_year = str(last_year)[-2:]
    future_year = str(future_year)[-2:]

    openFile = xlrd.open_workbook("AlumnosMatriculadosTFG.xls")
    number = len(openFile.sheet_names())

    print("Numero de hojas :",number)

    actual_course_name = name + actual_year + "_" + future_year
    actual_course_sheet = openFile.sheet_by_name(actual_course_name)
    actual_array = actual_course_sheet.col_values(0)
    actual_array.remove('administrador')
    actual_array.remove('DNI')
    actualYearlist = set(actual_array)


    if len(openFile.sheet_names()) >= 2:
        try:

            able=True
            print("Debería haber entrado aqui")
            last_course_name = name + last_year + "_" + actual_year
            last_course_sheet = openFile.sheet_by_name(last_course_name)

            past_array = last_course_sheet.col_values(0)
            past_array.remove('administrador')
            past_array.remove('DNI')


            pastYearlist = set(past_array)

            print("El conjunto de estudiantes del año actual es:")
            print(actualYearlist)

            print("El conjunto de estudiantes del año pasado es:")
            print(pastYearlist)

            commonUsers = actualYearlist & pastYearlist

        except XLRDError:
            print("No existe una hoja que haga referencia al año anterior")
            commonUsers = actualYearlist

    else:
        able=False

        print("Solo existe una hoja en el fichero de configuración, no se puede comparar con otro año")
        commonUsers = actualYearlist

        ''' while contador <= 10:
            if str(sheet.cell_value(contador, 1)) != "Alumno" and sheet.cell_value(contador, 1) != "administrador":
               pastYearlist = set(str(sheet.cell_value(contador, 0)))
            contador = contador + 1'''
        '''os.chdir(r'tutorial/static/config/')'''
    os.chdir(actualpath)
    print("AL ACABAR la lectura de los dni en común el path es: ", actualpath)
    return able,commonUsers

def get_active_course_name():
    today = date.today()

    actual_year = today.strftime("%Y")

    next_year = int(actual_year) + 1

    course_year = "Curso " + actual_year + "-" + str(next_year)

    return course_year

def get_past_course_name():
    today = date.today()

    actual_year = today.strftime("%Y")

    last_year = int(actual_year) - 1

    course_year = "Curso " + str(last_year) + "-" + actual_year

    return course_year

def move_past_student_to_actual_year(userlist, token):
    graph_client = OAuth2Session(token=token)
    course_year = get_past_course_name()
    found = False
    folder_id = get_active_id_folder(token)
    activefolderid = graph_client.get('{0}/me/drive/root:/Documentos/{1}/TFM Activos:/children'.format(graph_url, course_year))
    contador = 0
    for folder in activefolderid.json()['value']:
        print(folder['name'])
        for usercommon in userlist:
            if folder['name'].find(str(usercommon)) != -1:
                print("Se ha encontrado un alumno con el dni :" + str(usercommon) + "en la carpeta "+ folder['name'])
                contador = contador + 1
                result = graph_client.patch('{0}/me/drive/items/{1}'.format(graph_url, folder['id']),
                                           headers={'Content-Type': 'application/json'},
                                           json={
                                               "parentReference": {
                                                   "id": folder_id
                                               },
                                               "name": folder['name'],
                                               "@microsoft.graph.conflictBehavior" : "replace"
                                           })
                print(result.json())

                found = True
    print("El numero de carpetas movidas ha sido de: ", contador)
    return contador,found

def get_all_courses_in_active(token):
    graph_client = OAuth2Session(token=token)
    query_params = {
        '$select': 'name',
    }

    activecourses = graph_client.get('{0}/me/drive/root:/Documentos:/children'.format(graph_url),  params=query_params)
    return activecourses.json()


def get_user_files_selected_year(token, file_name):
    graph_client = OAuth2Session(token=token)

    query_params = {
        '$select': 'name,parentReference,id'
    }

    files = graph_client.get('{0}/me/drive/root:/Documentos/{1}/TFM Activos:/children'.format(graph_url,file_name),params=query_params)



    print(files.json())


        # Return the JSON result
    return files.json()

def get_user_files_readed_selected(token, course):
    graph_client = OAuth2Session(token=token)

    # Configure query parameters to
    # modify the results

    query_params = {
        '$select': 'name,parentReference,id'
    }
    course_year = course
    print("El curso: ",course)
    files = graph_client.get('{0}/me/drive/root:/Documentos/{1}/TFM Leidos:/children'.format(graph_url,course_year),params=query_params)


    print(files.json())

        # Return the JSON result
    return files.json()



def create_share_link(token, file_name, itemId, dict_teachers):
    graph_client = OAuth2Session(token=token)

    print("El itemId del fichero, "+ file_name + " es : "+ itemId)
    nombre = file_name.split('-')[0]
    # Configure query parameters to
    # modify the results


    files = graph_client.post('{0}/me/drive/items/{1}/createLink'.format(graph_url, itemId),
                                           headers={'Content-Type': 'application/json'},
                                            json = {
                                            "type": "embed",
                                            "scope": "anonymous"
                                            })




    '''print("A ver que devuelve el link creado del DriveItem" , files.json())

    print("El shareid deberia de ser el siguiente: ", files.json()['shareId'])'''

    sharingUrl = files.json()['link']['webUrl'];

    print("EL SHARING URL ES-------> : ", sharingUrl)
    '''base64Value = base64.b64encode(bytes(sharingUrl, 'utf-8'))


    #encodedUrl = "u!" + base64Value.strip('=').replace('/','_').replace('+','-')


    print("El tipo de basevalue es: ", type(base64Value))
    print("La url  es: ", base64Value)



    link = graph_client.get('{0}/shares/{1}'.format(graph_url, sharingUrl))


    print("EL LINK DEBERIA DE APARECER AQUI : ", link.json())'''

    subject = 'Acceso a carpeta de '+ nombre
    #message = 'Ha sido elegido para formar parte del tribunal de '+ nombre + '. A continuación desde este link podrá acceder a la carpeta en One Drive del alumno: ' + sharingUrl + '\nRecuerde que este link no se puede compartir con otros usuarios.\n\nMuchas gracias, un cordial saludo.'
    email_from = 'jorgeruiztfg2@hotmail.com'
    #recipient_list = ['jrperez4@esei.uvigo.es', ]

    for teacher in dict_teachers:
        list = []
        list.append(dict_teachers[teacher])
        message = 'Hola ' + teacher + ',\nHa sido elegido para formar parte del tribunal de ' + nombre + '. A continuación desde este link podrá acceder a la carpeta en One Drive del alumno: ' + sharingUrl + '\nRecuerde que este link no se puede compartir con otros usuarios.\n\nMuchas gracias, un cordial saludo.'
        send_mail(subject, message, email_from, list)

    #send_mail(subject, message, email_from, email_list)


    '''permission = graph_client.post('{0}/shares/{1}/permission/grant'.format(graph_url, url),
                              headers={'Content-Type': 'application/json'},
                              json={
                                  "recipients": [
                                     { "email": "jorgeruiztfg2@hotmail.com" }
                                        ],
                                  "roles": [ "read"]
                              })

    print("Después de haber realizado los permisos el PERMISSION es: ", permission.json())'''


    # Return the JSON result
    return files.json()

def check_if_admin_has_submit_documentation(token, file_name):

    graph_client = OAuth2Session(token=token)

    # Configure query parameters to
    # modify the results

    print("El nombre del file es : ", file_name)
    '''print("El valor del driveId es : ", driveId)
    print("El valor del ITEMID es : ", itemId)'''

    #files = graph_client.get('{0}/drives/{1}/items/{2}/children'.format(graph_url,driveId, itemId))
    course_year = get_active_course_name()


    files = graph_client.get('{0}/me/drive/root:/Documentos/{1}/TFM Activos:/children'.format(graph_url, course_year))

    print("--------------------------AQUI VIENEN LOS HIJOS DEL FICHERO---------------------------")
    print(files)
    # Return the JSON result
    return files.json()