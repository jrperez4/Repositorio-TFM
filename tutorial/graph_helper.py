# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# <FirstCodeSnippet>
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



# <GetFilesSnippet>
def get_user_shared_files(token):
    graph_client = OAuth2Session(token=token)



    # Configure query parameters to
    # modify the results

    # Send GET to /me/drive/root/children
    files = graph_client.get('{0}/me/drive/sharedWithMe'.format(graph_url))

    shared = graph_client.get('{0}/drives/33A0E52B21AB1E6D/items/33A0E52B21AB1E6D!109/children'.format(graph_url))

    '''/ drives / {remoteItem - driveId} / items / {remoteItem - id}'''

    print("--------------------------------------------------")

    #print("Drive id: " + files.json()['value'][0]['remoteItem']['parentReference']['driveId'])

   #print("Remote item id: " + files.json()['value'][0]['remoteItem']['id'])
    #print(files.json())
    print("----------------AQUI VA EL SHARED----------------------------------")
    print(shared.json()['value'])
    person = "1.0"
    id_user = get_folder_id_user(token, person)

    print("El id de la carpeta del usuario es: ", id_user)
    id_sourcecode, id_documentation, id_memoir = get_children_folder_ids(token, id_user)
    print("El id de la carpeta de codigo fuente del usuario es: ", id_sourcecode)
    print("El id de la carpeta de documentacion del usuario es: ", id_documentation)
    print("El id de la carpeta de memoria del usuario es: ", id_memoir)


    '''
    cadena = "Memoria"

    for person in shared.json()['value']:

       if person['name'].find(cadena) != -1:
           print(cadena+" forma parte de: ", person['name'].format(cadena))
           print("y su código es: ", person['id'])
       else:
           print(cadena + " NO forma parte de: ", person['name'].format(cadena))
           print("pero su código es: ", person['id'])

    



    print("----------------AQUI VA EL SHARED----------------------------------")
    print(shared.json()['value'][0])
    print("QUEREMOS VER 1 CARPETA",shared.json()['value'][0]['name'])
    print("Drive id: " + shared.json()['value'][0]['parentReference']['driveId'])
    print("Remote item id: " + shared.json()['value'][0]['parentReference']['id'])

     print("---------------------VA A LEER LOS ARCHIVOS-----------------------------")
     leer_archivos()
     print("---------------------ARCHIVOS LEIDOS-----------------------------")'''

    # Return the JSON result
    return files.json()
# </GetFilesSnippet>

def upload_file_to_onedrive(token):
    graph_client = OAuth2Session(token=token)

    files = graph_client.put('{0}/drives/33A0E52B21AB1E6D/items/33A0E52B21AB1E6D!110:/file:/content'.format(graph_url))

    return files.json()
# </GetFilesSnippet>

def get_folder_id_user(token,person):

    graph_client = OAuth2Session(token=token)
    shared = graph_client.get('{0}/drives/33A0E52B21AB1E6D/items/33A0E52B21AB1E6D!108/children'.format(graph_url))
    person_name = str(person)

    for person in shared.json()['value']:

       if person['name'].find(person_name) != -1:
           id = person['id']


    return id

def get_children_folder_ids(token,id_person):

    graph_client = OAuth2Session(token=token)
    shared = graph_client.get('{0}/drives/33A0E52B21AB1E6D/items/{1}/children'.format(graph_url,id_person))
    sourcecode = "Codigo Fuente"
    documentation = "Doc.TFM"
    memoir = "Memoria"


    for folder in shared.json()['value']:

        print("Carpeta: ", folder['name'], "con código ", folder['id'])
        if folder['name'].find(sourcecode)!= -1:
            id_sourcecode = folder['id']
        if folder['name'].find(documentation)!= -1:
            id_documentation = folder['id']
        if folder['name'].find(memoir) != -1:
            id_memoir = folder['id']


    return id_sourcecode,id_documentation,id_memoir

