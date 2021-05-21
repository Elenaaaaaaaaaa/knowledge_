from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='start'),
    path('registration', views.registration, name='registration'),
    path('login', views.loginP, name='login'),
    path('home', views.home, name='home'),

    path('projects', views.projects, name='projects'),
    path('project_create', views.project_create, name='project_create'),
    path('project_update/<str:pk>/', views.project_update, name='project_update'),
    path('project_delete/<str:pk>/', views.project_delete, name='project_delete'),

    path('userPage/<str:pk>/', views.UserPage, name='userPage'),
    path('user_delete/<str:pk>/', views.user_delete, name='user_delete'),

    path('projectPage/<str:pk>/', views.ProjectPage, name='projectPage'),
    path('doc_delete/<str:pk>/<str:i>/', views.doc_delete, name='doc_delete'),
    path('doc_create/<str:i>/', views.doc_create, name='doc_create'),
    path('doc_update/<str:pk>/<str:i>/', views.doc_update, name='doc_update'),
    path('project_Docs/<str:pk>/<str:i>/', views.project_Docs, name='project_Docs'),

    path('documentation/<str:pk>/', views.documentation, name='documentation'),
    path('documentation1/<str:pk>/', views.documentation1, name='documentation1'),
    path('documentation2/<str:pk>/', views.documentation2, name='documentation2'),

    path('task_comp/<str:pk>/<str:i>/', views.task_complete, name='task_complete'),
    path('task_add2/<str:pk>/', views.task_add2, name='task_add2'),

    path('taskPage', views.taskPage, name='tasks'),
    path('task_comp2/<str:pk>/<str:i>/', views.task_complete2, name='task_complete2'),
    path('task_uncomp/<str:i>/', views.task_uncomplete, name='task_uncomplete'),
    path('task_delete/<str:pk>/<str:i>/', views.task_delete, name='task_delete'),
    path('task_add/<str:pk>/', views.task_add, name='task_add'),

    path('logout', views.logoutU, name='logout'),
]
