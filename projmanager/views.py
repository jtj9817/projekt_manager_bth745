# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserForm, ProjectsForm
from django.views import generic
from django.views.generic import DetailView, View
from .models import Project, Organization, Application, Profile
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Permission
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from .utils import (ProfileGetObjectMixin)
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy, resolve


def index(request):
	return render(request, 'volunto/index.html')

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return render(request, 'volunto/index.html')
			else:
				return render(request, 'volunto/login.html', {'error_message': 'Account is disabled.'})
		else:
			return render(request, 'volunto/login.html', {'error_message': 'Invalid login'})
	return render(request, 'volunto/login.html')	

#User submits the form filled with data in a POST request
def register(request):
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			user= form.save(commit=False)
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user.set_password(password)
			user.save()
			user = authenticate(username=username, password=password)
			login(request, user)
			return render(request,'volunto/registersuccess.html')
	else:
		form = UserForm()
	return render(request, 'volunto/registration_form.html', {'form': form})


def logout_user(request):
	return render(request, 'volunto/logout.html')		

#Views for Projects 
class ProjectListView(LoginRequiredMixin,generic.ListView):
	model = Project
	context_object_name = 'projects_list'
	queryset = Project.objects.all()
	template_name = 'volunto/project_list.html'

	def get_queryset(self):
		return Project.objects.all()
	def get_context_data(self, **kwargs):
		context = super(ProjectListView, self).get_context_data(**kwargs)
		context['Temp data'] = 'Temp data for projects'
		return context

class ProjectDetailView(LoginRequiredMixin,generic.DetailView):
	model = Project
	template_name = "volunto/project_detail.html"

class ProjectCreate(LoginRequiredMixin,CreateView):
	model = Project
	fields = '__all__'

class ProjectUpdate(LoginRequiredMixin, UpdateView):
	model = Project
	fields = '__all__'
class ProjectDelete(LoginRequiredMixin,DeleteView):
	model = Project
	success_url = reverse_lazy('volunto:projects')

# Views for user Profile
@login_required
def edit_profile(request, pk):
	#Get User object from url
	user = User.objects.get(pk=pk)
	#Populate Profile form with values retrieved from db query using object above
	profile_form = UserForm(instance=user)
	ProfileInlineFormset = inlineformset_factory(User, Profile)
	formset = ProfileInlineFormset(instance=user)
	if request.user.is_authenticated() and request.user.id == user.id:
		if request.method == POST:
			user_form = UserForm(request.POST, instance=user)
			formset = ProfileInlineFormset(request.POST, instance=user)

			if user_form.is_valid():
				created_user = user_form.save(commit=False)
				formset = ProfileInlineFormset(request.POST, instance=created_user)

				if formset.is_valid():
					created_user.save()
					formset.save()
					return HttpResponseRedirect('/accounts/profile/')
		return render(request, "account/profile_update.html"),{
			"profile_render": pk,
			"profile_render_form": user_form,
			"formset": formset,
		}
	else:
		raise PermissionDenied

@method_decorator(login_required, name='dispatch')
class ProfileDetail(ProfileGetObjectMixin,DetailView):
	model = Profile

@method_decorator(login_required, name='dispatch')
class ProfileUpdate(ProfileGetObjectMixin,UpdateView):
	model = Profile
	fields = '__all__'

#These views are to be used in near future
@login_required
def join_project(request):
	if request.method == 'POST':
		form = ProjectsForm(request.POST)
		if form.is_valid():
			project = form.save(commit=False)
			projectname = form.cleaned_data.get('projectname')
			projdesc = form.cleaned_data.get('password')
			projstatus = form.cleaned_data.get('projstatus')
			project.save()
			return render(request,'volunto/project_success.html')
	else:
		form = ProjectsForm()
	return render(request, 'volunto/project_join.html')


