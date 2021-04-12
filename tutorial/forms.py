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

		'''def clean_title(self):
			title = self.cleaned_data["title"]
			if not title:
				return title

			if not title[0].isupper():
				self.add_error("title", "Should start with an uppercase letter")

			if title.endswith("."):
				self.add_error("title", "Should not end with a full stop")

			if "&" in title:
				self.add_error("title", "Use 'and' instead of '&'")

			description = self.cleaned_data["description"]

			if not description:
				return description
			if :
				self.add_error("title", "Should start with an uppercase letter")


			return title'''


