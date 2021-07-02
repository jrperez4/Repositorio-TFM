import os
import uuid


def random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.


def handle_uploaded_file(f):

  print("El nombre del fichero es :", f.name)
  print(os.getcwd())
  actualPath = os.getcwd()

  with open(r'tutorial/static/fileupload/' + f.name ,'wb+') as destination:
      for chunk in f.chunks():
          destination.write(chunk)

  print("Abriendo el handle el path es:",os.getcwd() )
  os.chdir(actualPath)
  print("Tras acabar el proceso el path vuelve a ser el mismo que antes: ",os.getcwd())


def handle_uploaded_file_memoir(f):
    print("El nombre del fichero es :", f)
    print("Y EL TIPO DE ARCHIVO ES: ", type(f))
    print(os.getcwd())
    actualPath = os.getcwd()

    header = f.name.split('.')[0]
    tail = f.name.split('.')[1]
    file_name_changed = header + "_" + random_string(6) + "." + tail
    f.name = file_name_changed
    '''if actualPath.find("config") != -1:
        print("En el path actual se encuentra el config: ", actualPath)
        os.chdir(r'../../../')
        os.chdir(r'tutorial/static/fileupload/')
        print("Lo encontró y ahora está en: ",os.getcwd())

    else:
        print("En el path actual no se encuentra el config: ", actualPath)'''

    with open(r'tutorial/static/fileupload/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    print("Abriendo el handle el path es:", os.getcwd())
    os.chdir(actualPath)
    print("Tras acabar el proceso el path vuelve a ser el mismo que antes: ", os.getcwd())
    print("El ARCHIVO DESDE EL HANDLE ES: ",f)
    print("Y EL TIPO DE ARCHIVO ES: ",type(f))
    return f