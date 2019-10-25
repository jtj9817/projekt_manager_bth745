# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .forms import UserForm, ProjectsForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic import DetailView, View, CreateView, UpdateView, DeleteView
from .models import Project, Organization, Profile
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy, resolve
from django.utils.decorators import method_decorator
from django.db import transaction
from django.contrib.auth import authenticate, login

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
				return render(request, 'index.html')
			else:
				return render(request, 'login.html', {'error_message': 'Account is disabled.'})
		else:
			return render(request, 'login.html', {'error_message': 'Invalid login'})
	return render(request, 'login.html')	

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
class ProjectListView(LoginRequiredMixin,generic.ListView):
	model = Project
	context_object_name = 'projects_list'
	queryset = Project.objects.all()
	template_name = 'project_list.html'

	def get_queryset(self):
		return Project.objects.all()
	def get_context_data(self, **kwargs):
		context = super(ProjectListView, self).get_context_data(**kwargs)
		context['Temp data'] = 'Temp data for projects'
		return context

class ProjectDetailView(LoginRequiredMixin,generic.DetailView):
	model = Project
	template_name = "project_detail.html"

class ProjectCreate(LoginRequiredMixin,CreateView):
	model = Project
	fields = '__all__'

class ProjectUpdate(LoginRequiredMixin, UpdateView):
	model = Project
	fields = '__all__'
class ProjectDelete(LoginRequiredMixin,DeleteView):
	model = Project
	success_url = reverse_lazy('volunto:projects')