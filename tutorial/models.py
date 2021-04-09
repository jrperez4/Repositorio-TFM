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
        user_id = models.OneToOneField(User, on_delete=models.SET_NULL, related_name="person", null=True, blank=True)
        title = models.CharField(max_length=50)
        keyword = models.CharField(max_length=50)
        description = models.CharField(max_length=50)
        sourcecode = models.FileField()
        documentation = models.FileField()
        memoir = models.FileField()
        id_folder = models.CharField(max_length=50)

        def __str__(self):
                return '%s %s' % (self.user_id, self.title)


