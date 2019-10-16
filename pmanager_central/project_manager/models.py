from django.db import models
from django.contrib.auth.models import User, Permission
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.validators import RegexValidator
# Create your models here.


class Organization(models.Model):
    orgname = models.CharField(max_length=200)
    orgdesc = models.TextField(max_length=200)
    orgid = models.AutoField(primary_key=True)
    orgusername = models.CharField(max_length=200)
    orgpw = models.CharField(max_length=30, default="")
    ORG_STATUS = (
        (1, 'Active'),
        (2, 'Inactive'),
        (3, 'In-review')
    )
    orgstat = models.PositiveIntegerField(choices=ORG_STATUS, default=3)

    def __str__(self):
        return self.orgname

    def get_absolute_url(self):
        # Returns a URL for accessing an Organization object instance
        return reverse('volunto:organization-detail', args=(self.orgid,))


class Project(models.Model):
    projectname = models.CharField("Project Name", max_length=200)
    projdesc = models.CharField("Project Description", max_length=500)
    projectid = models.AutoField(primary_key=True)
    projstatus = models.BooleanField("Project Status", default=False)
    project_deadline = models.DateTimeField(auto_now=False, auto_now_add=False, null=False)
    proj_created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.projectname
    def get_absolute_url(self):
        # Returns a URL for accessing a Project object instance
        return reverse('volunto:project-detail', args=(self.projectid,))


class Task(models.Model):
    taskid = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=128)
    task_description = models.TextField(max_length=256)
    TASK_PRIORITY = (
        (1, 'Low Priority'),
        (2, 'Medium Priority'),
        (3, 'High Priority')
    )
    task_priority = models.PositiveIntegerField(choices=TASK_PRIORITY, default=1)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.postitle


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=30, unique=True,
                            null=True, default=None)
    # Verbose name for Django Admin interface of Profile

    def __str__(self):
        return self.user.username

    # Use to redirect to Profile Update page
    def get_update_url(self):
        return reverse('dj-auth:profile_update')

    def get_absolute_url(self):
        return reverse('dj-auth:profile')
    # Methods to create and update Profile once a User was created

    def create_profile(sender, **kwargs):
        user = kwargs["instance"]
        if kwargs["created"]:
            user_profile = Profile(user=user)
            user_profile.save()
    post_save.connect(create_profile, sender=User)
