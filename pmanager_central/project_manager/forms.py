from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Organization, Profile
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
	username = forms.CharField(max_length=30,min_length=5)
	password = forms.CharField(widget=forms.PasswordInput)
	email = forms.EmailField(widget=forms.EmailInput, required=True)
	class Meta: 
		model = User
		fields = ['username', 'email', 'password']

	#Clean username data field to avoid conflict with URL slugging	
	def clean_username(self):
		username = self.cleaned_data['username']
		disallowed = ('activate', 'create', 'disable', 'login', 'logout', 'password', 'profile',)
		if username in disallowed:
			raise ValidationError("A user with that username already exists")
		return username

	#Clean email and check to see if user with same email is already registered
	def clean_email(self):
		email = self.cleaned_data.get('email')
		# Check to see if any users already exist with this email as a username.
		try:
			match = User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('This email address is already in use.')


class ProjectsForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['projectname', 'projdesc', 'projstatus']

#Form for User profile and to be extended using the Profile model
class UserCreationForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']