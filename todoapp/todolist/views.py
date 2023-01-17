from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required


@login_required
# Create your views here.
def index(request):
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")

    tasks = Task.objects.all()
    return render(request, "index.html", {"tasks": tasks, "task_form": form})


def update(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("index")
    return render(request, "update.html", {"edit_task_form": form})


def delete(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == "POST":
        task.delete()
        return redirect("index")
    return render(request, "delete.html", {"task": task})


from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login, authenticate
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Coucou {username}, Votre compte a été créé avec succès !')
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
