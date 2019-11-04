# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, ProjectsForm, TasksForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic import DetailView, View, CreateView, UpdateView, DeleteView, ListView
from django.views.generic.edit import FormView
from .models import Project, Organization, Profile
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy, resolve
from django.utils.decorators import method_decorator
from django.db import transaction
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
def index(request):
	return render(request, 'index.html')
def dashboard(request):
    return render(request, 'dashboard.html')
def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return render(request, 'dashboard.html')
			else:
				return render(request, 'login.html', {'error_message': 'Account is disabled.'})
		else:
			return render(request, 'login.html', {'error_message': 'Invalid login'})
	return render(request, 'dashboard.html')	

#User submits the form filled with data in a POST request
def register(request):
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			user= form.save(commit=False)
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			full_name = form.cleaned_data.get('full_name')
			user.set_password(password)
			user.save()
			user = authenticate(username=username, password=password)
			login(request, user)
			return render(request,'register_success.html')
	else:
		form = UserForm()
	return render(request, 'register.html', {'form': form})

#Function for updating prfoile, currently not used
@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _("Your profile was successfully updated!"))
        else:
            messages.error(request, _("Please correct the errors"))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, 'profile.html',{
		'user_form': user_form,
		'profile_form': profile_form
	})


#Views for Projects 
@login_required
@transaction.atomic
def project_create(request):
	if request.method == 'POST':
		form = ProjectsForm(request.POST)
		task_form = TasksForm(request.POST)
		if form.is_valid() & task_form.is_valid():
			project = form.save(commit=False)
			projectname = form.cleaned_data.get('projectname')
			projdesc = form.cleaned_data.get('projdesc')
			project_deadline = form.cleaned_data.get('project_deadline')
			project.save()
			return render(request,'project_success.html')
	else:
		form = ProjectsForm()
		task_form = TasksForm()
	return render(request, 'project_create.html', {'form': form, 'task_form': task_form})

class ProjectList(LoginRequiredMixin,ListView):
	model = Project
	context_object_name = 'projects_list'
	template_name = 'dashboard.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project_list'] = Project.objects.all()
		return context

class ProjectDetailView(LoginRequiredMixin,generic.DetailView):
	model = Project
	template_name = "project_detail.html"
 
class ProjectUpdateView(FormView):
	template_name = "project_update.html"
	#Retrieve Project object from the <pk> value passed through the URL parameters
	def get_object(self):
		id = self.kwargs.get('pk')
		obj = None
		if id is not None:
			obj = get_object_or_404(Project, projectid=id)
		return obj
	#Retrieve the ProjectsForm and TasksForm
	def get(self, request, id=None, *args, **kwargs):
		context = {}
		obj = self.get_object()
		if obj is not None:
			form = ProjectsForm(instance=obj)
			task_form = TasksForm()
			context['object'] = obj
			context['form'] = form
			context['task_form'] = task_form
		return render(request, self.template_name, context)

	def post(self, request, id=None, *args, **kwargs):
		context = {}
		obj = self.get_object()
		if obj is not None:
			form = ProjectsForm(request.POST, instance=obj)
			task_form = TasksForm()
			if form.is_valid():
				form.save()
			context['object'] = obj
			context['form'] = form
			context['task_form'] = task_form
		return render(request, self.template_name, context)

class ProjectDelete(LoginRequiredMixin,DeleteView):
	model = Project
	success_url = reverse_lazy('dashboard')
	success_message = "Project was deleted successfully!"