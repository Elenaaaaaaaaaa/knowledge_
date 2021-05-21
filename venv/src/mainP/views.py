from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, FileResponse
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import date

from .forms import *
from .models import *
from .filters import *

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


CLIENT_SECRET_FILE = 'mainP/client_secret.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']


def index(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, 'mainP/index.html')


def registration(request):
    form = CreateUserForm()
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')

                pk = User.objects.get(username=username)
                new_entry = Information(info_employee=pk)
                new_entry.save()

                messages.success(request, f'Account created for {username} ')
                return redirect("home")
        context = {"form": form}
        return render(request, "mainP/registration.html", context)


def loginP(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.info(request, "Логин или пароль неверный")
        context = {}
        return render(request, 'mainP/login.html', context)


def logoutU(request):
    logout(request)
    return redirect('start')


@login_required(login_url="start")
def home(request):
    pr = Projects.objects.filter(pr_team=request.user.id)
    comments_ = Comments.objects.all()
    context = {"projects": pr, "comments": comments_}
    print(request.user.id)
    return render(request, 'mainP/home.html', context)


# ---------PROJECT FORM--------------


@login_required(login_url="start")
def projects(request):
    amount = Projects.objects.count()
    projects_ = Projects.objects.all()
    amount2 = projects_.filter(pr_status='открыт').count()
    myFilt = ProjectFilter(request.GET, queryset=projects_)
    projects_ = myFilt.qs
    context = {"projects": projects_, "amount": amount, "amount_": amount2, "myFilt": myFilt}
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'mainP/projects.html', context)


@login_required(login_url="start")
def project_create(request):
    form = ProjectForm_create
    projects_ = Projects.objects.filter(pr_team=request.user.id)
    context = {'form': form, "projects": projects_ }
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects')
    return render(request, 'mainP/project_create.html', context)


@login_required(login_url="start")
def project_update(request, pk):
    pr = Projects.objects.get(id=pk)
    form = ProjectForm_create(instance=pr)
    projects_ = Projects.objects.filter(pr_team=request.user.id)
    context = {'form': form, "projects": projects_}
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=pr)
        if form.is_valid():
            form.save()
            return redirect('projects')
    return render(request, 'mainP/project_update.html', context)


@login_required(login_url="start")
def project_delete(request, pk):
    projects_ = Projects.objects.filter(pr_team=request.user.id)
    pr = Projects.objects.get(id=pk)
    context = {'item': pr, "projects": projects_}
    if request.method == 'POST':
        pr.delete()
        return redirect('projects')
    return render(request, 'mainP/project_delete.html', context)

# ---------USER FORM--------------


@login_required(login_url="start")
def UserPage(request, pk):
    info = Information.objects.filter(info_employee=pk)
    info_ = Information.objects.get(info_employee=pk)
    img = request.user.information.info_image.url
    projects_ = Projects.objects.all()
    form = UserInfoForm(instance=info_)
    context = {"form": form, "avatar": img, "inf": info, "inf_": info_, "projects": projects_}
    if request.method == 'POST':
        user = request.user.id
        form = UserInfoForm(request.POST, request.FILES, instance=info_)
        form.info_employee = user
        if form.is_valid():
            form.save()
            return redirect('userPage', user)
        print(form.errors)
    return render(request, 'mainP/userPage.html', context)


@login_required(login_url="start")
def user_delete(request, pk):
    pr = User.objects.get(id=pk)
    context = {'item': pr}
    if request.method == 'POST':
        pr.delete()
        return redirect('start')
    return render(request, 'mainP/user_delete.html', context)

# ---------PROJECT FORM--------------


@login_required(login_url="start")
def ProjectPage(request, pk):
    the_project = get_object_or_404(Projects, pr_name=pk)
    projects_ = Projects.objects.filter(pr_team=request.user.id)
    comments_ = Comments.objects.filter(com_proj=the_project.id)

    the_tasks = the_project.pr_task.all()
    act_t = the_tasks.filter(tk_status='актуально')
    act_tc = the_tasks.filter(tk_status='актуально').count()
    nact_t = the_tasks.filter(tk_status='выполнено')
    nact_tc = the_tasks.filter(tk_status='выполнено').count()

    docs = Documents.objects.all()
    documents_ = Documents.objects.filter(doc_project=the_project.id)[:5]
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        forma = form.save(commit=False)  # приостонови добавление формы
        forma.com_user = request.user
        forma.com_proj = the_project
        forma.save()

        if form.is_valid():
            form.save()

        return redirect('projectPage', the_project.pr_name)
        print(form.errors)

    d_count = docs.filter(doc_acc='принят').count()
    all_count = docs.count()
    context = {"projects": projects_, "the_project": the_project, "comments": comments_, "documents": documents_,
               "all_docs": all_count, "done_docs": d_count, "docs": docs, 'the_tasks': the_tasks,
               "act_t": act_t, "act_tc": act_tc, "nact_t": nact_t, "nact_tc": nact_tc, "form": form}
    return render(request, 'mainP/projectPage.html', context)


@login_required(login_url="start")
def task_complete(request, pk, i):
    tk = Tasks.objects.get(id=i)
    pr = Projects.objects.get(id=pk)
    tk.tk_status = 'выполнено'
    tk.save()
    return redirect('projectPage', pr.pr_name)


@login_required(login_url="start")
def task_add2(request, pk):
    projects_ = Projects.objects.filter(pr_team=request.user.id)
    pr = Projects.objects.get(id=pk)
    form = TaskForm()
    context = {'form': form, 'project': pr, 'projects': projects_}
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            the_task_name = form.cleaned_data['tk_name']
            the_task = Tasks.objects.get(tk_name=the_task_name)
            pr.pr_task.add(the_task)
            return redirect('projectPage', pr.pr_name)
    return render(request, 'mainP/task_add.html', context)

# ---------DOC FORMS--------------


@login_required(login_url="start")
def doc_delete(request, pk, i):
    projects_ = Projects.objects.filter(pr_team=request.user.id)
    pr = Documents.objects.get(id=pk)
    context = {'item': pr, 'i': i, "projects": projects_}
    if request.method == 'POST':
        pr.delete()
        return redirect('projectPage', i)
    return render(request, 'mainP/doc_delete.html', context)


@login_required(login_url="start")
def doc_create(request,  i):
    projects_ = Projects.objects.filter(pr_team=request.user.id)
    the_project = Projects.objects.get(id=i)
    form = DocForm_create
    context = {'form': form, 'projects': projects_}
    if request.method == 'POST':
        form = DocForm_create(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projectPage', the_project.pr_name)
        print(form.errors)
    return render(request, 'mainP/doc_create.html', context)


@login_required(login_url="start")
def doc_update(request, pk, i):
    projects_ = Projects.objects.filter(pr_team=request.user.id)
    pr = Documents.objects.get(id=pk)
    form = DocForm_update(instance=pr)
    context = {'form': form, 'i': i, "projects":projects_}
    if request.method == 'POST':
        form = DocForm_update(request.POST, instance=pr)
        if form.is_valid():
            form.save()
            return redirect('projectPage', i)
        print(form.errors)
    return render(request, 'mainP/doc_update.html', context)


@login_required(login_url="start")
def project_Docs(request, pk, i):
    the_project = Projects.objects.get(id=pk)
    projects_ = Projects.objects.filter(pr_team=request.user.id)
    comments_ = Comments.objects.filter(com_proj=the_project.id)

    docs = Documents.objects.all()
    documents_ = Documents.objects.filter(doc_project=the_project.id)

    if request.GET.get('q'):
        q = request.GET.get('q')
        documents_ = documents_.filter(doc_name=q)

    d_count = docs.filter(doc_acc='принят').count()
    all_count = docs.count()
    context = {"projects": projects_, "the_project": the_project, "comments": comments_, "documents": documents_,
               "all_docs": all_count, "done_docs": d_count, "docs": docs, "i": i}
    return render(request, 'mainP/project_Docs.html', context)


# ---------CALENDAR FORMS--------------
# @login_required(login_url="start")
# def calendar(request):
#     flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes=SCOPES)
#     flow.run_console()
#     pr = Projects.objects.filter(pr_team=request.user.id)
#     context = {"projects": pr}
#
#     return render(request, 'mainP/calendar.html', context)


@login_required(login_url="start")
def documentation(request, pk):
    context = {"pk": pk}
    return render(request, 'mainP/html/index.html', context)


@login_required(login_url="start")
def documentation1(request, pk):
    context = {"pk": pk}
    return render(request, 'mainP/html/genindex.html', context)


@login_required(login_url="start")
def documentation2(request, pk):
    context = {"pk": pk}
    return render(request, 'mainP/html/search.html', context)


# ---------Task FORMS--------------

@login_required(login_url="start")
def taskPage(request):
    projects_ = Projects.objects.filter(pr_team=request.user.id)

    hardest_count = Tasks.objects.filter(tk_dif='3', tk_status='актуально').count()
    hard_count = Tasks.objects.filter(tk_dif='4', tk_status='актуально').count()
    hard_act = hardest_count + hard_count
    easiest_count = Tasks.objects.filter(tk_dif='1', tk_status='актуально').count()
    easy_count = Tasks.objects.filter(tk_dif='2', tk_status='актуально').count()
    easy_act = easiest_count + easy_count

    nhardest_count = Tasks.objects.filter(tk_dif='3', tk_status='выполнено').count()
    nhard_count = Tasks.objects.filter(tk_dif='4', tk_status='выполнено').count()
    nhard_act = nhardest_count + nhard_count
    neasiest_count = Tasks.objects.filter(tk_dif='1', tk_status='выполнено').count()
    neasy_count = Tasks.objects.filter(tk_dif='2', tk_status='выполнено').count()
    neasy_act = neasiest_count + neasy_count

    act = Tasks.objects.filter(tk_status='актуально')
    not_act = Tasks.objects.filter(tk_status='выполнено')

    context = {"projects": projects_, 'hard_act': hard_act, 'easy_act': easy_act, 'act': act, 'not_act': not_act,
               'nhard_act': nhard_act, 'neasy_act': neasy_act}
    return render(request, 'mainP/taskPage.html', context)


@login_required(login_url="start")
def task_complete2(request, pk, i):
    tk = Tasks.objects.get(id=i)
    pr = Projects.objects.get(id=pk)
    tk.tk_status = 'выполнено'
    tk.save()
    return redirect('tasks')


@login_required(login_url="start")
def task_uncomplete(request, i):
    tk = Tasks.objects.get(id=i)
    tk.tk_status = 'актуально'
    tk.save()
    return redirect('tasks')


@login_required(login_url="start")
def task_delete(request, pk, i):
    tk = Tasks.objects.get(id=i)
    pr = Projects.objects.get(id=pk)
    pr.pr_task.remove(tk)
    return redirect('tasks')


@login_required(login_url="start")
def task_add(request, pk):
    projects_ = Projects.objects.filter(pr_team=request.user.id)
    pr = Projects.objects.get(id=pk)
    form = TaskForm()
    context = {'form': form, 'project': pr, 'projects': projects_}
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            the_task_name = form.cleaned_data['tk_name']
            the_task = Tasks.objects.get(tk_name=the_task_name)
            pr.pr_task.add(the_task)
            return redirect('tasks')
    return render(request, 'mainP/task_add.html', context)




