from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
from django.db import transaction
from ckeditor.fields import RichTextField

from django.forms import ModelForm
from django.forms import ModelForm, ClearableFileInput

from django.core.exceptions import ValidationError

#from tutorial.models import Usuario


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
		title = forms.CharField(max_length=30,label="Título")
		keyword = forms.CharField(max_length=30,label="Palabras clave")
		description = forms.CharField(max_length=120,widget=forms.Textarea(attrs={"rows":5, "cols":20}),label="Descripcion breve de TFM")
		sourcecode = forms.FileField(label="Código Fuente")
		documentation = forms.FileField(label="Justificante de defensa")
		memoir = forms.FileField(label="Memoria")

class uploadadmin(forms.Form):
	file_field = forms.FileField(label="Documentación del alumno",widget=forms.ClearableFileInput(attrs={'multiple': True}))
	'''summary = forms.FileField(label="Resumen",required=False)
	approval = forms.FileField(label="Visto Bueno",required=False)
	modality = forms.FileField(label="Modalidad de Defensa",required=False)
	report = forms.FileField(label="Informe del tutor",required=False)
	documentation = forms.FileField(label="Justificante de defensa",required=False)
	modifications = forms.FileField(label="Modificaciones del alumno",required=False)'''




