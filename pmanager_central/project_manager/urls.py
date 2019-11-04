from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.ProjectList.as_view(), name='dashboard'),
    path('project/create', views.project_create, name='project-create'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/delete/', views.ProjectDelete.as_view(), name='project-delete')
]

