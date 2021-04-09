from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
from django.db import transaction

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
		title = forms.CharField(max_length=50,label="Título")
		keyword = forms.CharField(max_length=50,label="Palabras clave")
		description = forms.CharField(max_length=50,label="Descripción breve")
		sourcecode = forms.FileField(label="Código Fuente")
		documentation = forms.FileField(label="Documentación")
		memoir = forms.FileField(label="Memoria")


'''class CustomClearableFileInput(ClearableFileInput):
	template_with_clear = '<br>  <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label> %(clear)s'


class FormEntrada(ModelForm):
	class Meta:
		model = Entrada
		fields = ('titulo', 'texto', 'archivo')
		widgets = {
			'archivo': CustomClearableFileInput
		}'''