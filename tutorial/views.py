# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
import json

from django.shortcuts import render, redirect
from xlutils.copy import copy

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from tutorial.forms import CreateUserForm, uploadadminrecord, createstudent, changetutors, searchfiles
from tutorial.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, \
    get_token
from tutorial.graph_helper import get_user, get_user_files, get_calendar_events, get_user_shared_files, \
    get_paths_to_upload, create_academic_course, move_single_folder_to_read, create_user_folder_in_active, \
    get_user_tutors, get_user_files_readed, get_active_course_name, get_dni_student_common, \
    move_past_student_to_actual_year, get_all_courses_in_active, get_user_files_selected_year, \
    get_user_files_readed_selected, create_share_link, check_if_admin_has_submit_documentation
import dateutil.parser
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse

from .forms import upload, uploadadmin
from tutorial.functions.functions import handle_uploaded_file, handle_uploaded_file_memoir
from requests_oauthlib import OAuth2Session
from tutorial.models import Bibliografia, Profesor
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import os
import xlrd
from django.views.generic import ListView
import uuid

'''from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders'''
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa




from django.http import FileResponse, Http404

graph_url = 'https://graph.microsoft.com/v1.0'
from datetime import date
import datetime


'''
from .forms import FormEntrada
from .models import Entrada'''



# <HomeViewSnippet>

def home(request):

    #if request.user.is_authenticated:
    context = initialize_context(request)

    if request.user.is_authenticated and request.user.username != 'administrador':

        if check_if_user_has_submit_his_documentation(request.user.username) is not False:
            context['documentation_uploaded'] = True

        else:
            context['documentation_uploaded'] = False


    return render(request, 'tutorial/home.html', context)
    #else:



# </HomeViewSnippet>

# <RegisterViewSnippet>
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid() and check_user(form.cleaned_data.get('username'),form.cleaned_data.get('email')):
                form.save()
                user = form.cleaned_data.get('username')
                '''username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')'''
                messages.success(request, 'Cuenta creada para ' + user)
                '''user = authenticate(request, username=username, password=password)'''
                return redirect('login')
            else:
              messages.warning(request, 'La cuenta no ha sido creada debido a:\n')
              messages.warning(request,'El email no pertenece a ningún estudiante matriculado')

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
                messages.warning(request, 'El DNI o la contraseña no son correctos.')

        context = {}

        return render(request, 'tutorial/login.html', context)


# <LoginViewSnippet>

def check_user(dni,correo):
    exists_user = False
    '''print("---------------------VA A LEER ARCHIVO DE PROFESORES-----------------------------")

    openFile = xlrd.open_workbook("D:\\Disco Duro\\Repositorio TFM COPIA\\tutorial\\ProfesoresESEI.xlsx")
    sheet = openFile.sheet_by_name("Profesorado")
    print("N. de filas", sheet.nrows)
    print("N de columnas", sheet.ncols)

    for i in range(sheet.nrows):
        print(sheet.cell_value(i, 0), "\t", sheet.cell_value(i, 1), "\t", sheet.cell_value(i, 2), "\t",
              sheet.cell_value(i, 3), "\t", sheet.cell_value(i, 4), "\t", sheet.cell_value(i, 5))'''

    '''print("---------------------VA A LEER ARCHIVO DE ALUMNOS-----------------------------")

    openFile = xlrd.open_workbook("D:\\TFG - Repositorio TFM\\Repositorio TFM\\tutorial\\AlumnosMatriculadosTFG.xlsx")
    sheet = openFile.sheet_by_name("Alumnado_20_21")
    print("N. de filas", sheet.nrows)
    print("N de columnas", sheet.ncols)'''

    print("---------------------VA A LEER ARCHIVO DE ALUMNOS-----------------------------")
    actualpath = os.getcwd()
    print("AL comprobar los datos de un USUARIO el path es:",actualpath)
    print("--------------------------EL PATH ACTUAL ES----------------------")
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

    for i in range(sheet.nrows):
        print("Alumno: ", sheet.cell_value(i,0))
        if str(sheet.cell_value(i,0)) == dni or sheet.cell_value(i,2) == correo:
            exists_user = True

            print("Se ha encontrado: " + str(sheet.cell_value(i,0))+ "es igual que "+ dni + " la persona es: ", sheet.cell_value(i,1))
            os.chdir(actualpath)
            return exists_user

    os.chdir(actualpath)
    print("------------------- EL PATH RESULTANTE---------------")
    print(os.getcwd())
    print("AL comprobar los datos de un USUARIO el path es:", os.getcwd())
    return exists_user




def logoutUser(request):
    print("El usuario que se está log out es:", request.user.username)
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
    print("EL TOKEN DESDE VIEW ES: ", token)

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

def bibliography(request):

    #queryset = request.GET.get("search")
    context = initialize_context(request)

    if request.user.is_authenticated is False or request.user.username != 'administrador':
        form = searchfiles()
        context = {'form': form}

        if request.method == "POST":
            form = searchfiles(request.POST)

            if form.is_valid():
                print("Titulo ->>>>", form.cleaned_data.get('text'))

                print("Opción ->>>>", form.cleaned_data.get('select'))


                if form.cleaned_data.get('select') and form.cleaned_data.get('text'):

                    texto = form.cleaned_data.get('text')

                    if form.cleaned_data.get('select') == 'Título':
                        print("Ha escogido el titulo")


                        #texto = texto.replace(" ", "")
                        print("Mucho texto---->", texto)

                        posts = Bibliografia.objects.filter(
                                Q(title__icontains=texto) &
                                Q(readed=True) &
                                Q(authorized_by_author=True)
                            ).distinct()

                        counter = 0
                        for post in posts:
                            counter = counter + 1
                            print("Query encontrada: ", post)

                        context = {'references': posts, 'times': counter, 'word' : texto , 'option' : form.cleaned_data.get('select') }

                        print("Contexto---->>", context)

                    if form.cleaned_data.get('select') == 'Palabras clave':
                        print("Ha escogido el Palabras clave")

                        texto = texto.replace(" ", "")
                        print("Mucho texto---->", texto)

                        posts = Bibliografia.objects.filter(
                            Q(keyword__icontains=texto) &
                            Q(readed=True)  &
                            Q(authorized_by_author=True)
                        ).distinct()

                        counter = 0
                        for post in posts:
                            counter = counter + 1
                            print("Query encontrada: ", post)

                        context = {'references': posts, 'times': counter, 'word': texto,
                                   'option': form.cleaned_data.get('select')}
                        print("Contexto---->>", context)

                    ''' if form.cleaned_data.get('select') == 'Descripción':
                        print("Ha escogido el Descripción")
    
                        texto = texto.replace(" ", "")
                        print("Mucho texto---->", texto)
    
                        posts = Bibliografia.objects.filter(
                            Q(description__icontains=texto) &
                            Q(readed=True) &
                            Q(authorized_by_author=True)
                        ).distinct()
    
                        counter = 0
                        for post in posts:
                            counter = counter + 1
                            print("Query encontrada: ", post)
    
                        context = {'references': posts, 'times': counter, 'word': texto,
                                   'option': form.cleaned_data.get('select')}
                        print("Contexto---->>", context)'''

                    if form.cleaned_data.get('select') == 'Autor':
                        print("Ha escogido el Autor")

                        texto = texto.replace(" ", "")
                        print("Mucho texto---->", texto)

                        posts = Bibliografia.objects.filter(
                            Q(author__icontains=texto) &
                            Q(readed=True) &
                            Q(authorized_by_author=True)
                        ).distinct()

                        counter = 0
                        for post in posts:
                            counter = counter + 1
                            print("Query encontrada: ", post)

                        context = {'references': posts, 'times': counter, 'word': texto,
                                   'option': form.cleaned_data.get('select')}
                        print("Contexto---->>", context)

                    if form.cleaned_data.get('select') == 'Tutor':
                        print("Ha escogido el Tutor")

                        texto = texto.replace(" ", "")
                        print("Mucho texto---->", texto)

                        posts = Bibliografia.objects.filter(
                            Q(tutor__icontains=texto) &
                            Q(readed=True)&
                            Q(authorized_by_author=True)
                        ).distinct()

                        counter = 0
                        for post in posts:
                            counter = counter + 1
                            print("Query encontrada: ", post)

                        context = {'references': posts, 'times': counter, 'word': texto,
                                   'option': form.cleaned_data.get('select')}
                        print("Contexto---->>", context)

                    if form.cleaned_data.get('select') == 'Cotutor':
                        print("Ha escogido el Cotutor")

                        texto = texto.replace(" ", "")
                        print("Mucho texto---->", texto)

                        posts = Bibliografia.objects.filter(
                            Q(cotutor__icontains=texto) &
                            Q(readed=True) &
                            Q(authorized_by_author=True)
                        ).distinct()

                        counter = 0
                        for post in posts:
                            counter = counter + 1
                            print("Query encontrada: ", post)

                        context = {'references': posts, 'times': counter, 'word': texto,
                                   'option': form.cleaned_data.get('select')}
                        print("Contexto---->>", context)

                    if form.cleaned_data.get('select') == 'Año':
                        print("Ha escogido el Año")

                        texto = texto.replace(" ", "")
                        print("Mucho texto---->", texto)

                        posts = Bibliografia.objects.filter(
                            Q(year=texto) &
                            Q(readed=True) &
                            Q(authorized_by_author=True)
                        ).distinct()

                        counter = 0
                        for post in posts:
                            counter = counter + 1
                            print("Query encontrada: ", post)

                        context = {'references': posts, 'times': counter, 'word': texto,
                                   'option': form.cleaned_data.get('select')}
                        print("Contexto---->>", context)
                else:
                    context = {'option': form.cleaned_data.get('select')}


            else:
                print("No ha entrado en el form como válido")


        return render(request, 'tutorial/searchfile.html', context)
    else:
        return HttpResponseRedirect(reverse('home'))



# <FilesViewSnippet>


@login_required(login_url='login')
def files(request, file_name=None):


    try:
        context = initialize_context(request)

        token = get_token(request)

        activecourses = get_all_courses_in_active(token)

        context['courses'] = activecourses['value']

        if file_name is None:
            if request.user.is_authenticated and request.user.username == "administrador":

                files = get_user_files(token)

                print("------------------------------LOS FICHEROS----------------------------")
                print(context['courses'])

                print("Es es lo que viene de One Drive: ----------------------", files['value'])

                for file in files['value']:
                    file_name = file['name']

                    print("El name del file es:", file['name'])
                    dni = file_name.split('-')[1]

                    print("El DNI del usuario es:", dni)

                    print("Aquí viene la comprobación de si ha entregado o existe una documentación a su nombre")

                    if check_if_user_has_submit_his_documentation(dni) is False:
                        file['status'] = 'No entregado'
                    else:
                        file['status'] = 'En Proceso'
                    if check_if_user_has_court(dni) is False:

                        file['court'] = 'No asignado'
                    else:
                        file['court'] = 'Asignado'

                    if check_if_admin_has_submit_documentation(dni) is False:
                        file['admin_documentation'] = 'No subida'
                    else:
                        file['admin_documentation'] = 'Subida'
                    if check_if_admin_has_submit_record(dni) is False:
                        file['admin_record'] = 'No subida'
                    else:
                        file['admin_record'] = 'Subida'


                context['files'] = files['value']

                print(context['files'])

                print("------------------------------LOS FICHEROS----------------------------")

                print("CONTEXTO................", context['files'])

                # print(files['value'][0]['createdBy']['application']['id'])
            else:
                return HttpResponseRedirect(reverse('home'))
        else:

            files = get_user_files_selected_year(token, file_name)

            for file in files['value']:
                file_name = file['name']
                print("El name del file es:", file['name'])
                dni = file_name.split('-')[1]

                print("El DNI del usuario es:", dni)

                print("Aquí viene la comprobación de si ha entregado o existe una documentación a su nombre")

                if check_if_user_has_submit_his_documentation(dni) is False:
                    file['status'] = 'No entregado'
                else:
                    file['status'] = 'En Proceso'
                if check_if_user_has_court(dni) is False:

                    file['court'] = 'No asignado'
                else:
                    file['court'] = 'Asignado'
                if check_if_admin_has_submit_documentation(dni) is False:
                    file['admin_documentation'] = 'No subida'
                else:
                    file['admin_documentation'] = 'Subida'
                if check_if_admin_has_submit_record (dni) is False:
                    file['admin_record'] = 'No subida'
                else:
                    file['admin_record'] = 'Subida'

            context['files'] = files['value']


            print("------------------------------LOS FICHEROS----------------------------")
            print(context['files'])
            print("------------------------------LOS CURSOS----------------------------")
            print(context['courses'])

        return render(request, 'tutorial/files.html', context)
    except KeyError as e:
        sign_in_url, state = get_sign_in_url()
        # Save the expected state so we can validate in the callback
        request.session['auth_state'] = state
        # Redirect to the Azure sign-in page
        return HttpResponseRedirect(sign_in_url)


# </FilesViewSnippet>

# <FilesReadedViewSnippet>
@login_required(login_url='login')
def files_readed(request, course=None):
    try:
        '''if request.user.is_authenticated and request.user.username == "administrador":
    
            context = initialize_context(request)
    
            token = get_token(request)
    
            files = get_user_files_readed(token)
    
            context['files'] = files['value']
    
            print("CONTEXTO................",context['files'])
    
            #print(files['value'][0]['createdBy']['application']['id'])
        else:
            return HttpResponseRedirect(reverse('home'))
    
        return render(request, 'tutorial/filesreaded.html', context)'''

        context = initialize_context(request)

        token = get_token(request)

        activecourses = get_all_courses_in_active(token)

        context['courses'] = activecourses['value']

        if course is None:
            if request.user.is_authenticated and request.user.username == "administrador":
                files = get_user_files_readed(token)

                print("------------------------------LOS FICHEROS----------------------------")
                print(context['courses'])

                if files['value'] != []:
                    for file in files['value']:
                        file_name = file['name']
                        print("El name del file es:", file['name'])
                        dni = file_name.split('-')[1]

                        print("El DNI del usuario es:", dni)

                        print("Aquí viene la comprobación de si ha entregado o existe una documentación a su nombre")

                        if check_if_user_has_submit_his_documentation(dni) is False:
                            file['status'] = 'No entregado'
                        else:
                            file['status'] = 'Defendido'



                    context['files'] = files['value']

                    print("------------------------------LOS FICHEROS----------------------------")

                    print("CONTEXTO................", context['files'])
                else:
                    messages.warning(request, "No hay ningún TFM presentado en el curso actual")
                    return HttpResponseRedirect(reverse('files'))
            else:
                return HttpResponseRedirect(reverse('home'))
        else:

            files = get_user_files_readed_selected(token, course)
            print("el files es--------------------------------: ", files)
            if files['value'] != []:

                for file in files['value']:
                    file_name = file['name']
                    print("El name del file es:", file['name'])
                    dni = file_name.split('-')[1]

                    print("El DNI del usuario es:", dni)

                    print("Aquí viene la comprobación de si ha entregado o existe una documentación a su nombre")

                    if check_if_user_has_submit_his_documentation(dni) is False:
                        file['status'] = 'No entregado'
                    else:
                        file['status'] = 'Defendido'

                context['files'] = files['value']
                print("------------------------------LOS FICHEROS----------------------------")
                print(context['files'])
                print("------------------------------LOS CURSOS----------------------------")
                print(context['courses'])
            else:
                messages.warning(request, "No hay ningún TFM presentado en el curso: "+ course)
                return HttpResponseRedirect(reverse('files'))

        return render(request, 'tutorial/filesreaded.html', context)
    except KeyError:
        sign_in_url, state = get_sign_in_url()
        # Save the expected state so we can validate in the callback
        request.session['auth_state'] = state
        # Redirect to the Azure sign-in page
        return HttpResponseRedirect(sign_in_url)

# </FilesReadedViewSnippet>

# <FilesViewSnippet>
def sharedfiles(request):
    context = initialize_context(request)

    token = get_token(request)

    print("TOKEN:",token)


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





def render_pdf_view(request):


    print("El usuario en cuestion es", request.user.username)
    dni = request.user.username
    filename = "resguardo_"+str(dni)+".pdf"
    query = Bibliografia.objects.filter(
        Q(dni__exact=dni)
    )
    print("Muestrame LA QUERY:",query)

    bibliografia = Bibliografia.objects.get(dni=dni)
    hour = bibliografia.upload_hour
    today = bibliografia.upload_date

    download_date = date.today()

    template_path = 'tutorial/resguardo.html'
    context = {'documentation': query, 'today': today, 'hour': hour}


    print("Muestrame el contexto:", context)
    # Create a Django response object, and specify content_type as pdf


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)


    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('Ha habido algún problema al generar el PDF <pre>' + html + '</pre>')
    return response


def pass_teachers_to_database():

    actualpath = os.getcwd()
    print("AL comprobar los datos de un USUARIO el path es:", actualpath)
    print("--------------------------EL PATH ACTUAL ES----------------------")
    os.chdir(r'tutorial/static/config/')
    openFile = xlrd.open_workbook("ProfesoresESEI.xlsx")
    sheet = openFile.sheet_by_index(0)



    for i in range(1, sheet.nrows):

        nombre_completo = str(sheet.cell_value(i, 0)) +" "+ str(sheet.cell_value(i, 1)) + " "+ str(sheet.cell_value(i, 2))
        departamento = str(sheet.cell_value(i, 3))
        area = str(sheet.cell_value(i, 4))
        correo = str(sheet.cell_value(i, 5))

        query = Profesor.objects.filter(
            Q(name=nombre_completo)
        )

        if len(query) == 0:
            profesor = Profesor(name=nombre_completo, departure=departamento, area=area, email=correo)
            profesor.save()

    print("Profesores---->", Profesor.objects.all())
    os.chdir(actualpath)
    print("------------------- EL PATH RESULTANTE---------------")
    print(os.getcwd())
    print("AL comprobar los datos de un USUARIO el path es:", os.getcwd())





def create_course(request):
    try:
        context = initialize_context(request)

        token = get_token(request)

        course_name = get_active_course_name()

        if not check_if_course_is_already_created(request):

            result = create_academic_course(token)

            var, userlist = get_dni_student_common()

            if var == True:
                print("Los estudiantes comunes son:")
                print(userlist)

                count,variable = move_past_student_to_actual_year(userlist, token)
                print("¿Se ha encontrado algún alumno?", variable)
                if count == 0:
                    messages.warning(request, "No se ha movido ningún estudiante del curso anterior")
                else:
                    messages.success(request,"Se han movido "+ str(count) + " estudiantes del año anterior")
            else:
                messages.warning(request,"No existe año anterior en el fichero de configuración")

            pass_teachers_to_database()
            context["folder"] = result

            messages.success(request, course_name + " creado con éxito")
        else:
            messages.warning(request,"El "+ course_name  +" ya ha sido creado")


        return render(request, 'tutorial/home.html', context)
    except KeyError:
        sign_in_url, state = get_sign_in_url()
        # Save the expected state so we can validate in the callback
        request.session['auth_state'] = state
        # Redirect to the Azure sign-in page
        return HttpResponseRedirect(sign_in_url)
# </FilesViewSnippet>

def check_if_course_is_already_created(request):

    created = False
    token = get_token(request)
    graph_client = OAuth2Session(token=token)

    root = graph_client.get('{0}/me/drive/root:/Documentos:/children'.format(graph_url))

    today = date.today()

    actual_year = today.strftime("%Y")

    future_year = int(actual_year) + 1

    course_year = "Curso " + actual_year + "-" + str(future_year)

    for folder in root.json()['value']:
        if folder['name'] == course_year:
            print("El curso con la carpeta: " + str(folder['name']) + " ya ha sido creado")
            created = True

        else:
            print("El curso actual: " + str(folder['name']) + " aún no ha sido creado")

    return created



def random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.




def upload_file(request):
    try:


      if not Bibliografia.objects.filter(Q(dni__exact=str(request.user.username))) or Bibliografia.objects.filter(Q(dni__exact=str(request.user.username)) & Q(uploaded=False)):

          token = get_token(request)
          form = upload()


          if request.method == "POST":
            form=upload(request.POST,request.FILES)

            if form.is_valid() and check_files(request,request.FILES['sourcecode'],request.FILES['documentation'],request.FILES['memoir']):

              print("Titulo ->>>>",form.cleaned_data.get('title'))
              print("Palabras clave ->>>>",form.cleaned_data.get('keyword'))
              print("Descripción ->>>>", form.cleaned_data.get('description'))
              print("Autoriza la divulgación de este TFM ->>>>", form.cleaned_data.get('authorization'))

              handle_uploaded_file(request.FILES['sourcecode'])
              handle_uploaded_file(request.FILES['documentation'])
              memoir_changed_name = handle_uploaded_file_memoir(request.FILES['memoir'])

              sourcecode = request.FILES['sourcecode']
              documentation = request.FILES['documentation']
              memoir = request.FILES['memoir']

              sourcecode_size = file_size(sourcecode)
              documentation_size = file_size(documentation)
              memoir_size = file_size(memoir_changed_name)


              path_memoir_content, path_memoir, path_sourcecode, path_documentation = get_paths_to_upload(token, request.user.username)


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
                  upload_file_min_size(memoir_changed_name, token, path_memoir)
              elif memoir_size >= 4000000:
                  upload_file_max_size(memoir_changed_name, token, path_memoir)
              else:
                  print("Error en el archivo memoir")

              author = request.user.first_name
              print("USUARIO->>>>>>>",type(author))
              dni = request.user.username
              tutor, cotutor = get_user_tutors(dni)
              print("El archivo de memoria es: ", memoir_changed_name)
              print("Y es de tipo:", type(memoir_changed_name))


              '''today = date.today()
              year = today.strftime("%Y")'''

              year = datetime.date.today().year
              month = datetime.date.today().month
              day = datetime.date.today().day

              date = str(day) + "-" + str(month) + "-" + str(year)

              hour = datetime.datetime.now().hour
              minute = datetime.datetime.now().minute

              if minute >=0 and minute<=9:
                  minute = str(minute)
                  minute = '0' + minute

              upload_time = str(hour) + ":" + str(minute)


              print("BIBLIO ANTES DE HABER SUBIDO---->", Bibliografia.objects.all())

              #Aqui va a ir la nueva modificación
              try:
                  bibliografia = Bibliografia.objects.get(dni=dni)
                  bibliografia.author = author
                  bibliografia.title = form.cleaned_data.get('title')
                  bibliografia.keyword=form.cleaned_data.get('keyword')
                  bibliografia.description=form.cleaned_data.get('description')
                  bibliografia.memoir=memoir_changed_name
                  bibliografia.id_folder=path_memoir_content
                  bibliografia.tutor=tutor
                  bibliografia.cotutor=cotutor
                  bibliografia.uploaded=True
                  bibliografia.authorized_by_author = form.cleaned_data.get('authorization')
                  bibliografia.upload_hour=upload_time
                  bibliografia.upload_date = date
                  bibliografia.year = year


                  bibliografia.save()
              except Bibliografia.DoesNotExist:
                  bibliografia = Bibliografia(dni=dni, author=author, title=form.cleaned_data.get('title'),
                                              keyword=form.cleaned_data.get('keyword'),
                                              description=form.cleaned_data.get('description'),
                                              memoir=memoir_changed_name, id_folder=path_memoir_content, tutor=tutor,
                                              cotutor=cotutor, readed=False, uploaded=True, authorized_by_author=form.cleaned_data.get('authorization'),upload_hour = upload_time,upload_date=date, first_court_member=None,
                                              second_court_member=None,
                                              third_court_member=None, admin_documentation=None, admin_record=None,
                                              year=year)


                  bibliografia.save()


              # Aqui acaba la nueva modificación'''

              ''' bibliografia = Bibliografia(dni=dni,author=author,title=form.cleaned_data.get('title'), keyword=form.cleaned_data.get('keyword'), description=form.cleaned_data.get('description'),
                                          memoir=memoir_changed_name,id_folder= path_memoir_content,tutor=tutor,cotutor=cotutor,readed=False, uploaded=True,first_court_member=None,second_court_member=None,
                                          third_court_member=None,admin_documentation=None, admin_record=None, year=year)'''


              print("BIBLIO DESPUES DE HABER SUBIDO---->",Bibliografia.objects.all())


              bibliografia.save()

              messages.success(request,'Archivos subidos con éxito puede descargar su resguardo aquí: <a href="downloadreceipt">Descargar</a>.')
              return HttpResponseRedirect(reverse('home'))
            else:
              jason = json.loads(form.errors.as_json())

              for key in jason.keys():

                if key == 'title':
                    messages.warning(request, "Título: " +  jason.get(key)[0].get("message"))
                if key == 'keyword':
                    messages.warning(request, "Palabras clave: " +  jason.get(key)[0].get("message"))
                if key == 'description':
                    messages.warning(request, "Justificante de defensa: " + jason.get(key)[0].get("message"))


              form=upload()


          return render(request,'tutorial/upload.html', {'form':form})
      else:
          messages.warning(request, "La documentación solo puede subirse una vez")
          return HttpResponseRedirect('home')

    except KeyError:
        sign_in_url, state = get_sign_in_url()
        # Save the expected state so we can validate in the callback
        request.session['auth_state'] = state
        # Redirect to the Azure sign-in page
        return HttpResponseRedirect(sign_in_url)



def upload_file_admin(request,file_id,file_name,course=None):
    try:
        token = get_token(request)
        form = uploadadmin()
        course_year = get_active_course_name()
        dni = file_name.split('-')[1]
        print("El dni del usuario es----->", dni)
        print("El id del file es:", file_id)
        print("El name del file es:", file_name)
        print("El name del curso es:", course)

        if course is not None:
            course_year = course

        path_admin = '/me/drive/root:/Documentos/{0}/TFM Activos/{1}/Documentacion/'.format(course_year,file_name)

        print("El request method es: ", request.method)

        if request.method == "POST":
            form = uploadadmin(request.POST, request.FILES)

            if form.is_valid():

                files = request.FILES.getlist('file_field')
                for file in files:
                    print("FILE: ", file)
                    handle_uploaded_file(file)
                    size = file_size(file)

                    if size < 4000000:
                        upload_file_min_size(file, token, path_admin)
                    elif size >= 4000000:
                        upload_file_max_size(file, token, path_admin)
                    else:
                        print("Error en el archivo source code")

                    print("TAMAÑO DEL FILE: ", size)

                messages.success(request, 'Documentacion subida para ' + file_name)


                print("BIBLIO ANTES DE QUE EL ADMIN SUBA LA DOCUMENTACION AL USUARIO---->", Bibliografia.objects.all())
                try:
                    bibliografia = Bibliografia.objects.get(dni=dni)
                    bibliografia.admin_documentation = True
                    bibliografia.save()
                except Bibliografia.DoesNotExist:
                    bibliografia = Bibliografia(dni=dni, author=None, title=None,
                                                keyword=None,
                                                description=None,
                                                memoir=None, id_folder=None, tutor=None,
                                                cotutor=None, readed=False, uploaded=False, authorized_by_author= None, upload_hour=None,upload_date=None,first_court_member=None,
                                                second_court_member=None,
                                                third_court_member=None, admin_documentation=True, admin_record=None,
                                                year=None)
                    bibliografia.save()
                print("BIBLIO DESPUES DE QUE EL ADMIN SUBA LA DOCUMENTACION AL USUARIO---->", Bibliografia.objects.all())


                return HttpResponseRedirect(reverse('files'))






            else:
                print("El formulario no es valido:   ", form)




        return render(request, 'tutorial/uploadfileadmin.html', {'form':form})
    except KeyError:
        sign_in_url, state = get_sign_in_url()
        # Save the expected state so we can validate in the callback
        request.session['auth_state'] = state
        # Redirect to the Azure sign-in page
        return HttpResponseRedirect(sign_in_url)


def upload_record_file_admin(request,file_id,file_name,course=None):

    dni = file_name.split('-')[1]

    if check_if_user_has_court(dni) is False:
        messages.warning(request,"El usuario no tiene asignado un tribunal todavía, no se pueden subir actas.")
        return HttpResponseRedirect(reverse('files'))

    token = get_token(request)
    form = uploadadminrecord()
    course_year = get_active_course_name()
    print("El id del file es:", file_id)
    print("El name del file es:", file_name)
    print("El name del curso es:", course)

    if course is not None:
        course_year = course

    path_admin = '/me/drive/root:/Documentos/{0}/TFM Activos/{1}/Actas/'.format(course_year, file_name)

    print("El request method es: ", request.method)

    if request.method == "POST":
        form = uploadadminrecord(request.POST, request.FILES)
        files = request.FILES.getlist('record')
        print("El tipo de archivo es:             ", type(files))
        if form.is_valid() and check_admin_files(request, files):

            for file in files:
                print("FILE: ", file)
                handle_uploaded_file(file)
                size = file_size(file)

                if size < 4000000:
                    upload_file_min_size(file, token, path_admin)
                elif size >= 4000000:
                    upload_file_max_size(file, token, path_admin)
                else:
                    print("Error en el archivo de subida")

                print("TAMAÑO DEL FILE: ", size)

            messages.success(request, 'Acta subida para ' + file_name)

            print("BIBLIO ANTES DE QUE EL ADMIN SUBA LA DOCUMENTACION AL USUARIO---->", Bibliografia.objects.all())
            try:
                bibliografia = Bibliografia.objects.get(dni=dni)
                bibliografia.admin_record = True
                bibliografia.save()
            except Bibliografia.DoesNotExist:
                bibliografia = Bibliografia(dni=dni, author=None, title=None,
                                            keyword=None,
                                            description=None,
                                            memoir=None, id_folder=None, tutor=None,
                                            cotutor=None, readed=False, uploaded=False, authorized_by_author=None, upload_hour=None,upload_date=None, first_court_member=None,
                                            second_court_member=None,
                                            third_court_member=None, admin_documentation=None, admin_record=True,
                                            year=None)
                bibliografia.save()
            print("BIBLIO DESPUES DE QUE EL ADMIN SUBA LA DOCUMENTACION AL USUARIO---->", Bibliografia.objects.all())

            return HttpResponseRedirect(reverse('files'))


        else:
            print("El formulario no es valido:   ", form)
            messages.warning(request,
                             "No se cumple con la extensión, los archivos solo pueden ser .docx, .dot, .dotm, .xlsx")

    return render(request, 'tutorial/uploadadminrecord.html', {'form': form})



def file_size(file):
    file.seek(0, os.SEEK_END)
    return file.tell()


def check_admin_files(request,file_list):
    valid_files = False

    for file in file_list:

        if file.name.find(".docx") != -1 or file.name.find(".dot") != -1 or file.name.find(".dotm") != -1 or file.name.find(".xlsx") != -1:
           valid_files = True

        else:
            messages.warning(request, "El fichero: " + file.name + " no es formato PDF")
            valid_files = False
            return valid_files

    return valid_files



def check_files(request,file, file2, file3):
    valid_files  = False

    if file.name.find(".zip") != -1 or file.name.find(".rar") != -1 or file.name.find(".7z") != -1 or file.name.find(".ZIP") != -1 or file.name.find(".RAR") != -1 or file.name.find(".7Z") != -1:
        if file2.name.find(".pdf") != -1 or file2.name.find(".PDF") != -1:
            if file3.name.find(".pdf") != -1 or file3.name.find(".PDF") != -1:
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

def move_user_to_read(request,file_id,file_name, course=None):


    try:

        dni = file_name.split("-")[1]
        name = file_name.split("-")[0]

        #referencia = Bibliografia.objects.get(dni=dni)

        context = initialize_context(request)


        if Bibliografia.objects.get(dni=dni) is not None:

            referencia = Bibliografia.objects.get(dni=dni)
            print("LA BIBLIOGRAFIA NO ES NULA")
            print("Bibliografia antes: --------->", referencia)
            referencia.readed = True;
            referencia.save()

            token = get_token(request)

            if course is not None:
                move_single_folder_to_read(token, file_id, file_name, course)
            else:
                move_single_folder_to_read(token, file_id, file_name)

            files = get_user_files(token)

            context['files'] = files['value']

            print(context['files'])
            print("Bibliografia despues: --------->", referencia)

    except ObjectDoesNotExist:
        token = get_token(request)
        files = get_user_files(token)
        context['files'] = files['value']
        messages.warning(request,  name + " aún no ha añadido su documentación")
        return HttpResponseRedirect(reverse('files'))

    messages.success(request, 'La documentación de ' + name + " ha sido movida a leída")

    return HttpResponseRedirect(reverse('files'))

    '''print("request........................")
    context = initialize_context(request)

    token = get_token(request)

    move_single_folder_to_read(token,file_id,file_name)

    files = get_user_files(token)

    context['files'] = files['value']

    print(context['files'])

    dni = file_name.split("-")[1]

    referencia = Bibliografia.objects.get(dni=dni)
    print("Bibliografia antes: --------->",referencia)
    referencia.readed=True;
    referencia.save()

    print("Bibliografia despues: --------->", referencia)


    messages.success(request, 'La documentación de ' + file_name + " ha sido movida a leída")

    return HttpResponseRedirect(reverse('files'))'''



def create_student_file(request):

    token = get_token(request)

    print("El método de request es: ",request.method)

    form = createstudent()

    if request.method == "POST":
        form = createstudent(request.POST)

        if form.is_valid():

            user_name = form.cleaned_data.get('student_name')
            user_surname = form.cleaned_data.get('student_surname')


            #name_changed = user_name.split(" ")[1] + " "+ user_name.split(" ")[2] + " " + user_name.split(" ")[0]
            dni = form.cleaned_data.get('dni')
            user_folder = user_surname + " " + user_name + "-" + dni
            email = form.cleaned_data.get('email')
            tutor = form.cleaned_data.get('tutor')
            cotutor = form.cleaned_data.get('cotutor')

            if check_user(dni,email) is False:

                '''list = []
                list.append(dni)
                list.append(user_name)
                list.append(email)
                list.append(tutor)'''

                actualpath = os.getcwd()
                print("AL comprobar los datos de un USUARIO el path es:", actualpath)
                print("--------------------------EL PATH ACTUAL ES----------------------")
                os.chdir(r'tutorial/static/config/')

                name = "Alumnado_"

                today = date.today()

                actual_year = today.strftime("%Y")[-2:]

                last_year = int(actual_year) - 1
                future_year = int(actual_year) + 1

                future_year = str(future_year)[-2:]

                actual_course_name = name + actual_year + "_" + future_year

                openFile = xlrd.open_workbook("AlumnosMatriculadosTFG.xls")

                sheet = openFile.sheet_by_name(actual_course_name)

                wb = copy(openFile)

                for each in range(openFile.nsheets):
                    sheet = openFile.sheet_by_index(each)
                    if str(actual_course_name) == str(sheet.name):
                        print("La posición de la hoja del año actual ("+ str(sheet.name) + ") es :" + str(each))
                        s = wb.get_sheet(each)


                if cotutor is None:
                    s.write(sheet.nrows, 0, dni)
                    s.write(sheet.nrows, 1, user_name)
                    s.write(sheet.nrows, 2, email)
                    s.write(sheet.nrows, 3, str(tutor))
                else:
                    s.write(sheet.nrows, 0, dni)
                    s.write(sheet.nrows, 1, user_name)
                    s.write(sheet.nrows, 2, email)
                    s.write(sheet.nrows, 3, str(tutor))
                    s.write(sheet.nrows, 4, str(cotutor))

                wb.save("AlumnosMatriculadosTFG.xls")

                print("........FICHERO DE ALUMNOS.........")
                for i in range(1, sheet.nrows):
                    print("ALUMNO--> " + str(i) + ' : ' + "\t" + str(sheet.cell_value(i, 0)) + "\t" + str(
                        sheet.cell_value(i, 1)) + "\t" + str(sheet.cell_value(i, 2)))
                print("........FIN DE ALUMNOS.........")



                os.chdir(actualpath)
                print("------------------- EL PATH RESULTANTE---------------")
                print(os.getcwd())
                print("AL comprobar los datos de un USUARIO el path es:", os.getcwd())


            else:
                messages.warning(request, "Ya existe un alumno con ese email o DNI.")
                return render(request, 'tutorial/createstudentfile.html', {'form':form})

            create_user_folder_in_active(token, user_folder)
            messages.success(request, 'Se ha creado una carpeta a nombre de ' + user_folder)

            return HttpResponseRedirect(reverse('files'))


        else:
            print("El formulario no es valido:   ", form)
            messages.warning(request, "El formulario no es válido:")


    return render(request, 'tutorial/createstudentfile.html', {'form':form})

def detailed_file(request, dni=None):

    if dni is not None:
        context = initialize_context(request)
        print("El parámetro opcional es :", dni)



        query = Bibliografia.objects.filter(
                Q(dni__exact=dni) &
                Q(readed=True)
        ).distinct()


        print("Query encontrada: ", query)

        context = {'documentation': query}
        return render(request, 'tutorial/detailedfile.html', context)
    else:
        return HttpResponseRedirect(reverse('home'))

def check_if_user_has_submit_his_documentation(dni):
    submit = False
    try:
        if Bibliografia.objects.get(dni=dni) is not None:
            referencia = Bibliografia.objects.get(dni=dni)
            print("Aquí va la referencia a nombre del usuario con el dni" + dni)
            if referencia.uploaded is True:
                submit = True

    except ObjectDoesNotExist:
       ''' messages.warning(request,
                         "El usuario todavía no ha entregado su documentación, no se puede asignar un tribunal")'''
       submit = False

    return submit




def check_if_user_has_court(dni):
    submit = False
    try:
        if Bibliografia.objects.get(dni=dni) is not None:
            referencia = Bibliografia.objects.get(dni=dni)
            if referencia.first_court_member is not None and referencia.second_court_member is not None and referencia.third_court_member is not None:
                submit = True
            print("Aquí va la referencia a nombre del usuario con el dni" + dni)
            print(referencia)



    except ObjectDoesNotExist:
        ''' messages.warning(request,
                          "El usuario todavía no ha entregado su documentación, no se puede asignar un tribunal")'''
        submit = False

    return submit

def check_if_admin_has_submit_documentation(dni):
    submit = False
    try:
        if Bibliografia.objects.get(dni=dni) is not None:
            referencia = Bibliografia.objects.get(dni=dni)
            print("¿Ha añadido algún tipo de documentación el administrador?: ", referencia.admin_documentation)
            if referencia.admin_documentation is True:
               submit = True
            print("Aquí va la referencia a nombre del usuario con el dni" + dni)
            print(referencia)


    except ObjectDoesNotExist:

       submit = False

    return submit

def check_if_admin_has_submit_record(dni):
    submit = False
    try:
        if Bibliografia.objects.get(dni=dni) is not None:
            referencia = Bibliografia.objects.get(dni=dni)
            print("¿Ha añadido las actas el administrador?: ", referencia.admin_documentation)
            if referencia.admin_record is True:
               submit = True
            print("Aquí va la referencia a nombre del usuario con el dni" + dni)
            print(referencia)


    except ObjectDoesNotExist:

       submit = False

    return submit


def change_tutors(request, file_name, id_file, course=None):

    token = get_token(request)
    print("El name del file es:", file_name)
    dni = file_name.split('-')[1]

    print("El DNI del usuario es:", dni)

    print("Aquí viene la comprobación de si ha entregado o existe una documentación a su nombre")
    if check_if_user_has_submit_his_documentation(dni) is False:
        messages.warning(request,"El usuario todavía no ha entregado su documentación, no se puede asignar un tribunal.")
        return HttpResponseRedirect(reverse('files'))

    else:
        form = changetutors()

        print("El request method es: ", request.method)

        if request.method == "POST":
            form = changetutors(request.POST)

            if form.is_valid() and form.cleaned_data.get('primermiembro') is not None and form.cleaned_data.get('segundomiembro') is not None and form.cleaned_data.get('tercermiembro') is not None:


                primermiembro = form.cleaned_data.get('primermiembro')
                segundomiembro = form.cleaned_data.get('segundomiembro')
                tercermiembro = form.cleaned_data.get('tercermiembro')
                print("El primer miembro del tribunal escogido es: ", primermiembro)
                print("El tipo del miembro: ", type(primermiembro))
                print("El segundo miembro del tribunal escogido es: ", segundomiembro)
                print("El tipo del miembro: ", type(segundomiembro))
                print("El tercer miembro del tribunal escogido es: ", tercermiembro)
                print("El tipo del miembro: ", type(tercermiembro))




                try:

                    if Bibliografia.objects.get(dni=dni) is not None:
                        referencia = Bibliografia.objects.get(dni=dni)
                        print("LA BIBLIOGRAFIA NO ES NULA")
                        print("Bibliografia antes: --------->", referencia)
                        referencia.first_court_member = str(primermiembro)
                        referencia.second_court_member = str(segundomiembro)
                        referencia.third_court_member = str(tercermiembro)

                        first_member = Profesor.objects.get(name=str(primermiembro))
                        print("En principio el segundo miembro del tribunal tiene como email:", first_member.email)
                        first_member.email = 'ruizperezjorge1@gmail.com'
                        first_member_email = first_member.email
                        print("El email cambiado del primer profesor es: ", first_member_email)
                        second_member = Profesor.objects.get(name=str(segundomiembro))
                        print("En principio el segundo miembro del tribunal tiene como email:", second_member.email)
                        second_member.email = 'jrperez4@esei.uvigo.es'
                        second_member_email = second_member.email
                        print("El email cambiado del segundo profesor es: ", second_member_email)
                        third_member = Profesor.objects.get(name=str(tercermiembro))
                        print("En principio el tercer miembro del tribunal tiene como email:",  third_member.email)
                        third_member.email = 'jorgeruizpeamazon@gmail.com'
                        third_member_email = third_member.email
                        print("El email cambiado del tercer profesor es: ", third_member_email)

                        dict_teachers = {}

                        dict_teachers[str(primermiembro)] = first_member_email
                        dict_teachers[str(segundomiembro)] = second_member_email
                        dict_teachers[str(tercermiembro)] = third_member_email

                        referencia.save()
                        create_share_link(token, file_name, id_file, dict_teachers)

                except ObjectDoesNotExist:

                    messages.warning(request, "El usuario todavía no ha entregado su documentación, no se puede asignar un tribunal")
                    return HttpResponseRedirect(reverse('files'))


                    messages.warning(request, "El usuario todavía no ha entregado su documentación, no se puede asignar un tribunal")
                    return HttpResponseRedirect(reverse('files'))

                messages.success(request, 'Tribunal asignado para ' + file_name)
                return HttpResponseRedirect(reverse('files'))


            else:

                messages.warning(request, "Deben escogerse los tres miembros del tribunal.")

        return render(request, 'tutorial/selecttutors.html', {'form': form})



def show_pdf(request,memoir):

    print("Encontro el pdf",memoir)

    try:
        with open('tutorial/static/fileupload/'+ memoir, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename='+ memoir
            return response
        pdf.closed
    except:
        messages.warning(request, memoir + " no se ha encontrado")
        return HttpResponseRedirect(reverse('detailedfile'))



def category_list(request):
    data = {
        'title': 'Listado de Categorías',
        'categories': Bibliografia.objects.all()
    }
    return render(request, 'tutorial/filelist.html', data)


class CategoryListView(ListView):
    model = Bibliografia
    template_name = 'tutorial/filelist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Bibliografia'
        return context

