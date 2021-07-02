'''from django.db import models
from django.db.models.signals import post_save
from localflavor.es.forms import ESIdentityCardNumberField
from werkzeug.security import generate_password_hash as genph
from werkzeug.security import check_password_hash as checkph
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password

# Create your models here.


class Usuario(AbstractUser):
    #user_id = ESIdentityCardNumberField(only_nif=True)
    validado = models.BooleanField(default=False)


class Profesor(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    departamento = models.CharField(max_length=50)
    area = models.CharField(max_length=50)


class Alumno(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Profesor, related_name='tutor', on_delete=models.CASCADE)
    cotutor = models.ForeignKey(Profesor, related_name='cotutor', on_delete=models.CASCADE)


from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dni = models.CharField(max_length=9)
    email = models.EmailField(max_length=30)
    name = models.CharField(max_length=20)
    surname1 = models.CharField(max_length=20)
    surname2 = models.CharField(max_length=20)
    tutor = models.CharField(max_length=50)
    cotutor = models.CharField(max_length=50)

   def __str__(self):
   return self.email
'''''''''

from django.db import models
from django.contrib.auth.models import User

class Bibliografia(models.Model):
        dni = models.CharField(max_length=50)
        author = models.CharField(max_length=50,null=True)
        title = models.CharField(max_length=50,null=True)
        keyword = models.CharField(max_length=50,null=True)
        description = models.CharField(max_length=200,null=True)
        memoir = models.FileField(max_length=200,null=True)
        id_folder = models.CharField(max_length=50,null=True)
        tutor =  models.CharField(max_length=50,null=True)
        cotutor = models.CharField(max_length=50,null=True)
        readed = models.BooleanField(default=False,null=True)
        uploaded = models.BooleanField(default=False,null=True)
        authorized_by_author = models.BooleanField(default=False,null=True)
        upload_hour = models.CharField(max_length=50,null=True)
        upload_date = models.CharField(max_length=50, null=True)
        first_court_member = models.CharField(max_length=50,null=True)
        second_court_member = models.CharField(max_length=50,null=True)
        third_court_member = models.CharField(max_length=50,null=True)
        admin_documentation = models.BooleanField(default=False,null=True)
        admin_record = models.BooleanField(default=False,null=True)
        year = models.CharField(max_length=50,null=True)


        def __str__(self):
                return 'Autor: %s , DNI: %s, Título: %s, Archivo: %s , Enlace para documentación: %s, Leido: %s, Año: %s, TFM entregado: %s,Fecha de entrega: %s, Hora de entrega: %s , Documentación aportada por admin: %s, Acta subida: %s , Autorizado por el autor: %s' % (self.author,self.dni,self.title, self.memoir,self.id_folder,self.readed, self.year, self.uploaded,self.upload_date,self.upload_hour,self.admin_documentation,self.admin_record, self.authorized_by_author)

class Profesor(models.Model):
        name = models.CharField(max_length=100)
        departure = models.CharField(max_length=50)
        area = models.CharField(max_length=50)
        email = models.CharField(max_length=50)

        def __str__(self):
                return '%s' % (self.name)
'''     
class CursoAcademico(models.Model):
        id_curso = models.CharField(max_length=50, primary_key=True)
        year = models.CharField(max_length=50)
        bibliografy = models.ForiegnKey(Bibliografia, on_delete=models.CASCASE)

        def __str__(self):
                return 'ID_Curso: %s , Year: %s, Bibliografia: %s' % (self.id_curso, self.year, self.bibliografy)'''
