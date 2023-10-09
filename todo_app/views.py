import datetime
import json
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Todo
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    name = request.user.username
    if request.method == 'POST':
        task = request.POST['task']
        date = request.POST['date']
        print(date)
        todo = Todo.objects.create(username=request.user.username, task=task, created_at=date)
        todo.save()
        return redirect(reverse(index))
    completed = Todo.objects.filter(username=request.user.username, completed=True)
    todos = Todo.objects.filter(username=request.user.username, completed=False, created_at__gte=datetime.date.today())
    expired = Todo.objects.filter(username=request.user.username, completed=False, created_at__lt=datetime.date.today())
    return render(request, "index.html", {'name':name, 'todos': todos, 'completed': completed, 'expired': expired,})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = User.objects.create_user(username, password=password)
            user.email = email
        
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "messages": ["Username already taken."]
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
        

    return render(request, "register.html")

def login_view(request):
    if request.method != "POST":
        return (
            HttpResponseRedirect(reverse("index"))
            if request.user.is_authenticated
            else render(request, "login.html")
        )
    # Attempt to sign user in
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    # Check if authentication successful
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        messages.error(request, "Invalid username and/or password.")
        return redirect(reverse(login_view))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


@csrf_exempt
def delete_todo(request, identifier):
    if request.method == 'POST':
        try:
            todo = Todo.objects.get(id=identifier, username=request.user.username)
            todo.delete()
            return JsonResponse({'status': 200, 'msg': "Todo deleted"}, status=200)
        except Todo.DoesNotExist:
            return JsonResponse({'status': 404, 'msg': "The todo doesn't seem to exist"}, status=404)
    else:
        redirect(reverse(index))
        
@csrf_exempt
def update_todo(request, identifier):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            todo = Todo.objects.get(id=identifier, username=request.user.username)
            todo.task = body['updatedTask']
            todo.created_at = body['updatedDate']
            todo.save()
            return JsonResponse({'status': 200, 'msg': "Todo updated"}, status=200)
        except Todo.DoesNotExist:
            return JsonResponse({'status': 404, 'msg': "The todo doesn't seem to exist"}, status=404)
    else:
        redirect(reverse(index))

@csrf_exempt
def toggle_complete_todo(request, identifier):
    if request.method == 'POST':
        try:
            todo = Todo.objects.get(id=identifier, username=request.user.username)
            todo.completed = not todo.completed
            todo.save()
            return JsonResponse({'status': 200, 'msg': "Todo completed"}, status=200)
        except Todo.DoesNotExist:
            return JsonResponse({'status': 404, 'msg': "The todo doesn't seem to exist"}, status=404)
    else:
        redirect(reverse(index))