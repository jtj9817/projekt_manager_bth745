from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Organization, Profile, Task
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from flatpickr import DateTimePickerInput


class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=30, min_length=5, widget=forms.TextInput(
        attrs={'placeholder': 'Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter your password'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Enter your email'}), required=True)
    full_name = forms.CharField(label='Full Name', max_length=30, min_length=4, required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'}))

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password']

    # Clean username data field to avoid conflict with URL slugging
    def clean_username(self):
        username = self.cleaned_data['username']
        disallowed = ('activate', 'create', 'disable', 'login',
                      'logout', 'password', 'profile',)
        if username in disallowed:
            raise ValidationError("A user with that username already exists")
        return username

    # Clean email and check to see if user with same email is already registered
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('This email address is already in use.')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name']


class TasksForm(forms.ModelForm):
    task_name = forms.CharField(label= 'Task Name', widget=forms.TextInput(
        attrs={'placeholder': 'Enter the task name'}))
    task_description = forms.CharField(label= 'Task Description', widget=forms.Textarea(
        attrs={'placeholder': 'Describe the task in 30 words or less'}))
    class Meta:
        model = Task
        fields = ['task_name', 'task_description', 'task_priority']


class ProjectsForm(forms.ModelForm):
    projectname = forms.CharField(label='Project Name', max_length=30, min_length=5, widget=forms.TextInput(
        attrs={'placeholder': 'Enter the project name'}))
    projdesc = forms.CharField(label='Project Description', widget=forms.Textarea(
        attrs={'placeholder': 'Describe the project in 500 characters'}), required=True)
    project_deadline = forms.DateTimeField(
        label='Project Deadline Date', widget=DateTimePickerInput(), required=True)

    class Meta:
        model = Project
        fields = ['projectname', 'projdesc', 'project_deadline']     
        
# Form for User profile and to be extended using the Profile model
class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
