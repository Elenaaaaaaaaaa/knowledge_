from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class CreateUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProjectForm(ModelForm):
    class Meta:
        model = Projects
        fields = '__all__'


class ProjectForm_create(ModelForm):
    class Meta:
        model = Projects
        fields = '__all__'


class UserInfoForm(ModelForm):
    class Meta:
        model = Information
        fields = ['info_job', 'info_tel', 'info_image']


class DocForm_create(ModelForm):
    class Meta:
        model = Documents
        fields = '__all__'


class DocForm_update(ModelForm):
    class Meta:
        model = Documents
        fields = '__all__'


class CommentForm(ModelForm):

    class Meta:
        model = Comments
        fields = ['com_title', 'com_text', 'com_teg']


class TaskForm(ModelForm):

    class Meta:
        model = Tasks
        fields = '__all__'




