from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login_user/', views.login_user, name='login_user'),
    path('dashboard/', views.ProjectList.as_view(), name='dashboard'),
    path('projects/create', views.ProjectCreate.as_view(), name='project-create'),
    path('projects/<int:pk>', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/<int:pk>', views.ProjectUpdate.as_view(), name='project-update'),
    path('project/<int:pk>/delete', views.ProjectDelete.as_view(), name='project-delete')
]

