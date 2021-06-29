from django.core import paginator
from todolist_app.models import TaskList
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from todolist_app.forms  import TaskForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False).task_owner = request.user
            form.save()
            messages.success(request,("New Task Added!"))
        return redirect('todolist')
    else:
        all_tasks = TaskList.objects.filter(task_owner=request.user)
        paginator = Paginator(all_tasks, 10)
        page = request.GET.get('page')
        all_tasks = paginator.get_page(page)
        return render(request , 'todolist.html', {'all_tasks': all_tasks})

@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.task_owner == request.user:
        task.delete()
    else:
        messages.error(request,("ACCESS RESTRICTED, You Are Not Allowed!!"))
    return redirect('todolist')

@login_required
def edit_task(request , task_id):
         if request.method == "POST":
                task = TaskList.objects.get(pk=task_id)
                form = TaskForm(request.POST or None, instance=task)
                if form.is_valid():
                    form.save()
                messages.success(request,("Task Edited!"))
                return redirect('todolist')
         else:
                task_obj = TaskList.objects.get(pk=task_id)
                return render(request , 'edit.html', {'task_obj':task_obj})

@login_required
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.task_owner == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request,("ACCESS RESTRICTED, You Are Not Allowed!!"))
    return redirect('todolist')

@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.task_owner == request.user:
        task.done = False
        task.save()
    else:
        messages.error(request,("ACCESS RESTRICTED, You Are Not Allowed!!"))
    return redirect('todolist')

def contact(request):
    context = {
        'contact_text':"Welcome To Contact Us Page."
    }
    return render(request , 'contact.html', context)

def about(request):
    context = {
        'about_text':"Welcome To About Us Page."
    }
    return render(request , 'about.html', context)

def index(request):
    context = {
        'index_text':"Welcome To Index Page."
    }
    return render(request , 'index.html', context)