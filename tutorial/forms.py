import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
from django.db import transaction
from localflavor.es.forms import ESIdentityCardNumberField

from ckeditor.fields import RichTextField

from django.forms import ModelForm
from django.forms import ModelForm, ClearableFileInput

from django.core.exceptions import ValidationError

#from tutorial.models import Usuario
from tutorial.models import Profesor


class AlumnoLogin(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'email', 'password1', 'password2']

	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.validado = False;
		user.save()
		return user

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'email', 'password1', 'password2']

	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.validado = False;
		user.save()
		return user

class upload(forms.Form):
		title = forms.CharField(max_length=50,label="Título")
		keyword = forms.CharField(max_length=50,label="Palabras clave")
		description = forms.CharField(max_length=200,widget=forms.Textarea(attrs={"rows":5, "cols":20}),label="Descripción breve de TFM")
		sourcecode = forms.FileField(label="Código Fuente")
		documentation = forms.FileField(label="Justificante de defensa")
		memoir = forms.FileField(label="Memoria")
		authorization = forms.BooleanField(required=False, disabled=False,widget=forms.widgets.CheckboxInput(attrs={'class': 'checkbox-inline'}),help_text="Autorizo la visualización del contenido de este trabajo a través de Internet, así como su repoducción, grabación en soporte informático o impresión para su uso privado o con fines de investigación.",error_messages={'required': "Please check the box"})


class uploadadmin(forms.Form):
	file_field = forms.FileField(label="Documentación del alumno",widget=forms.ClearableFileInput(attrs={'multiple': True}))
	'''summary = forms.FileField(label="Resumen",required=False)
	approval = forms.FileField(label="Visto Bueno",required=False)
	modality = forms.FileField(label="Modalidad de Defensa",required=False)
	report = forms.FileField(label="Informe del tutor",required=False)
	documentation = forms.FileField(label="Justificante de defensa",required=False)
	modifications = forms.FileField(label="Modificaciones del alumno",required=False)'''
class uploadadminrecord(forms.Form):
	record = forms.FileField(label="Actas del alumno", widget=forms.ClearableFileInput(attrs={'multiple': True}))

class createstudent(forms.Form):
	student_name = forms.CharField(max_length=30, label="Nombre del alumno")
	student_surname = forms.CharField(max_length=50, label="Apellidos del alumno")
	dni = ESIdentityCardNumberField(only_nif=True, label="Dni del alumno",max_length=9)
	email =	forms.EmailField(max_length=200, label="Email")
	tutor = forms.ModelChoiceField(label="Tutor",queryset=Profesor.objects.all().order_by('name'), required=True, widget=forms.Select(attrs={'class':'form-control', 'style':'width:20em;'}))
	cotutor = forms.ModelChoiceField(label="Cotutor",queryset=Profesor.objects.all().order_by('name'), required=False, widget=forms.Select(attrs={'class':'form-control', 'style':'width:20em;'}))


class changetutors(forms.Form):

	primermiembro = forms.ModelChoiceField(label="Primer miembro del Tribunal",queryset=Profesor.objects.all().order_by('name'), required=False, widget=forms.Select(attrs={'class':'form-control', 'style':'width:20em;'}))
	segundomiembro = forms.ModelChoiceField(label="Segundo miembro del Tribunal",queryset=Profesor.objects.all().order_by('name'), required=False, widget=forms.Select(attrs={'class':'form-control', 'style':'width:20em;'}))
	tercermiembro = forms.ModelChoiceField(label="Tercer miembro del Tribunal",queryset=Profesor.objects.all().order_by('name'), required=False, widget=forms.Select(attrs={'class':'form-control', 'style':'width:20em;'}))

class searchfiles(forms.Form):
	options =  (('Título', 'Título'),('Palabras clave', 'Palabras clave'),
				('Autor', 'Autor'),('Tutor', 'Tutor'),('Cotutor', 'Cotutor'),('Año', 'Año'))

	select = forms.ChoiceField(choices=options,label="Opciones",required=False)
	text = forms.CharField(max_length=50, label="Titulo", required=False)
		#date = forms.DateField(widget=forms.SelectDateWidget(years=YEARS), required=False,label="Año")