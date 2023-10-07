from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages

def index(request):
    name = request.user.username
    return render(request, "index.html", {'name':name})

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
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

# Create your views here.
