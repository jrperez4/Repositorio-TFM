# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
import json

from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from tutorial.forms import CreateUserForm
from tutorial.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, \
    get_token
from tutorial.graph_helper import get_user, get_user_files, get_calendar_events, get_user_shared_files, get_paths_to_upload, create_academic_course
import dateutil.parser
from django.contrib import messages
from django.http import HttpResponseRedirect

from .forms import upload
from tutorial.functions.functions import handle_uploaded_file
from requests_oauthlib import OAuth2Session
from tutorial.models import Bibliografia
from django.contrib.auth.models import User

import os
import xlrd

graph_url = 'https://graph.microsoft.com/v1.0'


'''
from .forms import FormEntrada
from .models import Entrada'''

# <HomeViewSnippet>
@login_required(login_url='login')
def home(request):

    if request.user.is_authenticated:
        context = initialize_context(request)
        return render(request, 'tutorial/home.html', context)
    else:
        return redirect('login')


# </HomeViewSnippet>

# <RegisterViewSnippet>
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid() and check_user(request,form.cleaned_data.get('username'),form.cleaned_data.get('email')):
                form.save()
                user = form.cleaned_data.get('username')
                '''username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')'''
                messages.success(request, 'Account was created for ' + user)
                '''user = authenticate(request, username=username, password=password)'''
                return redirect('login')
            else:
              messages.warning(request, 'Account was not created due to:\n')

        print(form)
        context = {'form': form}
        return render(request, 'tutorial/register.html', context)


# <RegisterViewSnippet>

# <LoginViewSnippet>
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            print("USERNAME Y CONTRASEÑA ",username,password)

            user = authenticate(request, username=username, password=password)
            print("EL USUARIO CAMBIADO",user)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}

        return render(request, 'tutorial/login.html', context)


# <LoginViewSnippet>

def check_user(request,dni,correo):
    exists_user = False
    print("---------------------VA A LEER ARCHIVO DE PROFESORES-----------------------------")

    openFile = xlrd.open_workbook("D:\\Disco Duro\\Repositorio TFM COPIA\\tutorial\\ProfesoresESEI.xlsx")
    sheet = openFile.sheet_by_name("Profesorado")
    print("N. de filas", sheet.nrows)
    print("N de columnas", sheet.ncols)

    for i in range(sheet.nrows):
        print(sheet.cell_value(i, 0), "\t", sheet.cell_value(i, 1), "\t", sheet.cell_value(i, 2), "\t",
              sheet.cell_value(i, 3), "\t", sheet.cell_value(i, 4), "\t", sheet.cell_value(i, 5))

    print("---------------------VA A LEER ARCHIVO DE ALUMNOS-----------------------------")

    openFile = xlrd.open_workbook("D:\\TFG - Repositorio TFM\\Repositorio TFM\\tutorial\\AlumnosMatriculadosTFG.xlsx")
    sheet = openFile.sheet_by_name("Alumnado_20_21")
    print("N. de filas", sheet.nrows)
    print("N de columnas", sheet.ncols)


    for i in range(sheet.nrows):

        if str(sheet.cell_value(i,0)) == dni and sheet.cell_value(i,2) == correo:
            exists_user = True
            print("Se ha encontrado: " + str(sheet.cell_value(i,0))+ "es igual que "+ dni + " el personaje es: ", sheet.cell_value(i,1))
            return exists_user


    return messages.warning(request,'Email does not match with DNI')


def logoutUser(request):
    logout(request)
    return redirect('login')


# <InitializeContextSnippet>
def initialize_context(request):
    context = {}

    # Check for any errors in the session
    error = request.session.pop('flash_error', None)

    if error != None:
        context['errors'] = []
        context['errors'].append(error)

    # Check for user in the session
    context['user'] = request.session.get('user', {'is_authenticated': False})
    return context


# </InitializeContextSnippet>

# <SignInViewSnippet>
def sign_in(request):
    # Get the sign-in URL
    sign_in_url, state = get_sign_in_url()
    # Save the expected state so we can validate in the callback
    request.session['auth_state'] = state
    # Redirect to the Azure sign-in page
    return HttpResponseRedirect(sign_in_url)


# </SignInViewSnippet>

# <SignOutViewSnippet>
def sign_out(request):
    # Clear out the user and token
    remove_user_and_token(request)

    return HttpResponseRedirect(reverse('home'))


# </SignOutViewSnippet>

# <CallbackViewSnippet>
def callback(request):
    # Get the state saved in session
    expected_state = request.session.pop('auth_state', '')
    # Make the token request
    token = get_token_from_code(request.get_full_path(), expected_state)

    # Get the user's profile
    user = get_user(token)

    # Save token and user
    store_token(request, token)
    store_user(request, user)

    return HttpResponseRedirect(reverse('home'))
# </CallbackViewSnippet>

# <CalendarViewSnippet>
def calendar(request):
    context = initialize_context(request)

    token = get_token(request)

    events = get_calendar_events(token)

    print("Aqui va el contexto", context, "Aqui acaba!!!!!!!!!!!!!!!")
    if events:
        # Convert the ISO 8601 date times to a datetime object
        # This allows the Django template to format the value nicely
        for event in events['value']:
            event['start']['dateTime'] = dateutil.parser.parse(event['start']['dateTime'])
            event['end']['dateTime'] = dateutil.parser.parse(event['end']['dateTime'])

        context['events'] = events['value']

    return render(request, 'tutorial/calendar.html', context)


# </CalendarViewSnippet>


# <FilesViewSnippet>
def files(request):
    context = initialize_context(request)

    token = get_token(request)

    files = get_user_files(token)

    context['files'] = files['value']

    print(files['value'][0]['createdBy']['application']['id'])

    return render(request, 'tutorial/files.html', context)


# </FilesViewSnippet>

# <FilesViewSnippet>
def sharedfiles(request):
    context = initialize_context(request)

    token = get_token(request)

    files = get_user_shared_files(token)

    if files:
        # Convert the ISO 8601 date times to a datetime object
        # This allows the Django template to format the value nicely
        for file in files['value']:
            print('ID: ', file['remoteItem']['parentReference']['driveId'])
            print('Remote Item ID: ', file['remoteItem']['id'])
            print('Name: ', file['remoteItem']['name'])
            print('Size: ', file['remoteItem']['size'], "\n")



    context['files'] = files['value']


    return render(request, 'tutorial/sharedfiles.html', context)
# </FilesViewSnippet>

def create_course(request):
    context = initialize_context(request)

    token = get_token(request)

    result = create_academic_course(token)

    context["folder"] = result

    return render(request, 'tutorial/home.html', context)
# </FilesViewSnippet>


def upload_file(request):
  token = get_token(request)
  form = upload()


  if request.method == "POST":
    form=upload(request.POST,request.FILES)

    if form.is_valid() and check_files(request,request.FILES['sourcecode'],request.FILES['documentation'],request.FILES['memoir']):
      print("Titulo ->>>>",form.cleaned_data.get('title'))
      print("Palabras clave ->>>>",form.cleaned_data.get('keyword'))
      print("Descripción ->>>>", form.cleaned_data.get('description'))

      handle_uploaded_file(request.FILES['sourcecode'])
      handle_uploaded_file(request.FILES['documentation'])
      handle_uploaded_file(request.FILES['memoir'])

      sourcecode = request.FILES['sourcecode']
      documentation = request.FILES['documentation']
      memoir = request.FILES['memoir']

      sourcecode_size = file_size(sourcecode)
      documentation_size = file_size(documentation)
      memoir_size = file_size(memoir)

      path_memoir, path_sourcecode, path_documentation = get_paths_to_upload(token, request.user.username)


      if sourcecode_size < 4000000:
          upload_file_min_size(sourcecode, token, path_sourcecode)
      elif sourcecode_size >= 4000000:
          upload_file_max_size(sourcecode, token, path_sourcecode)
      else:
          print("Error en el archivo source code")

      if documentation_size < 4000000:
          upload_file_min_size(documentation, token, path_documentation)
      elif documentation_size >= 4000000:
          upload_file_max_size(documentation, token, path_documentation)
      else:
          print("Error en el archivo documentation")


      if memoir_size < 4000000:
          upload_file_min_size(memoir, token, path_memoir)
      elif memoir_size >= 4000000:
          upload_file_max_size(memoir, token, path_memoir)
      else:
          print("Error en el archivo memoir")

      '''user = User.objects.get(id=request.user.id)
      print("USUARIO->>>>>>>",type(user))


      bibliografia = Bibliografia(user=user,title=form.cleaned_data.get('title'), keyword=form.cleaned_data.get('keyword'), description=form.cleaned_data.get('description'),sourcecode=request.FILES['sourcecode'],documentation=request.FILES['documentation'],memoir=request.FILES['memoir'],id_folder=folder_id)
      print("BIBLIO---->",bibliografia)
      bibliografia.save()'''

      return HttpResponseRedirect(reverse('home'))
    else:
      jason = json.loads(form.errors.as_json())

      for key in jason.keys():

        if key == 'title':
            messages.warning(request, "Título: " +  jason.get(key)[0].get("message"))
        if key == 'keyword':
            messages.warning(request, "Palabras clave: " +  jason.get(key)[0].get("message"))
        if key == 'description':
            messages.warning(request, "Descripción: " + jason.get(key)[0].get("message"))


      form=upload()




  return render(request,'tutorial/upload.html', {'form':form})

def file_size(file):
    file.seek(0, os.SEEK_END)
    return file.tell()





def check_files(request,file, file2, file3):
    valid_files  = False

    if file.name.find(".zip") != -1 or file.name.find(".rar") != -1 or file.name.find(".7z") != -1:
        if file2.name.find(".pdf") != -1:
            if file3.name.find(".pdf") != -1:
                valid_files = True
            else:
                print("El fichero: ", file3.name , " no es formato PDF")
                messages.warning(request,"El fichero: "+ file3.name + " no es formato PDF")
        else:
            print("El fichero: ", file2.name , " no es formato PDF")

            messages.warning(request, "El fichero: "+ file2.name + " no es formato PDF")
    else:
        print("El fichero: ", file.name, " no cumple con la extensión comprimida")
        messages.warning(request, "El fichero: "+ file.name + " no cumple con la extensión comprimida")

    return valid_files


def upload_file_min_size(file,token,path):

    graph_client = OAuth2Session(token=token)

    graph_client.put('{0}{1}{2}:/content'.format(graph_url, path, file),
                     headers={
                         'Authorization': 'Bearer ' + str(token),
                         'Content-type': 'application/binary'
                     },
                     data=open('tutorial/static/fileupload/' + file.name, 'rb').read())


def upload_file_max_size(file,token,path):

    graph_client = OAuth2Session(token=token)
    result = graph_client.post('{0}{1}{2}:/createUploadSession'.format(graph_url,path, file),
                     headers={'Authorization': 'Bearer ' + str(token)},
                     json={
                         '@microsoft.graph.conflictBehavior': 'replace',
                         'description': 'A large test file',
                         'fileSystemInfo': {'@odata.type': 'microsoft.graph.fileSystemInfo'},
                         'name': file.name
                     })

    upload_session = result.json()
    upload_url = upload_session['uploadUrl']


    st = os.stat('tutorial/static/fileupload/'+file.name)
    size = st.st_size
    CHUNK_SIZE = 10485760
    chunks = int(size / CHUNK_SIZE) + 1 if size % CHUNK_SIZE > 0 else 0

    with open('tutorial/static/fileupload/'+file.name, 'rb') as fd:
        start = 0
        for chunk_num in range(chunks):
            chunk = fd.read(CHUNK_SIZE)
            bytes_read = len(chunk)
            upload_range = f'bytes {start}-{start + bytes_read - 1}/{size}'
            print(f'chunk: {chunk_num} bytes read: {bytes_read} upload range: {upload_range}')
            result = graph_client.put(
                upload_url,
                headers={
                    'Content-Length': str(bytes_read),
                    'Content-Range': upload_range
                },
                data=chunk
            )
            result.raise_for_status()
            start += bytes_read
