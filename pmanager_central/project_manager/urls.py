from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    #path(r'^login_user/$', views.login_user, name='login_user'),
    #path(r'^logout_user/$', views.logout_user, name='logout_user'),
    #path(r'^accounts/update/(?P<pk>[\-\w]+)/$', views.edit_profile, name='account_update'),
    #path(r'^profile/$',views.ProfileDetail.as_view(), name="profile"),
    #path(r'^profile/edit/$', views.ProfileUpdate.as_view(), name="profile_update")
]

