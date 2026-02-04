from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if user exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # 🔥 AUTO LOGIN
        login(request, user)

        messages.success(request, "Account created successfully")
        return redirect('home')   # home page

    return render(request, "userapp/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "userapp/login.html")



def logout_view(request):
    logout(request)
    return redirect('home')
