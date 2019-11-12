from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.ProjectList.as_view(), name='dashboard'),
    path('home/', views.home, name='home'),
    path('project/create', views.project_create, name='project-create'),
    path('project/<int:pk>', views.project_details, name='project-detail'),
    path('project/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/update/second', views.ProjectUpdateView2, name='project-update-second'),
    path('project/<int:pk>/delete/', views.ProjectDelete.as_view(), name='project-delete')
    #path('project/<int:pk>/update/tasks', views.UpdateTasks, name='project-tasks')
]

