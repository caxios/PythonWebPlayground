from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def register(request):
    if request.method == "POST":
        username = request.POST['username'] # request.POST.get('username')
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # checking infomations of newly registering user whether duplicated in database or not.
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                print("username is already exist! try another one")
                return redirect("register")
            else:
                if User.objects.filter(email=email).exists():
                    print("email already exist! try another one")
                    return redirect("register")
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    return redirect("login")
        else:
            print("passwords not match!")
            return redirect("register")
    else:
        return render(request, "accounts/register.html")
    
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is None:
            print("invalid information")
            return redirect("login")
        else:
            auth.login(user)
            print("login successful")
            return redirect("showProducts")
    else:
        return render(request, "accounts/login.html")
    
def logout(request):
    if request.method == "POST":
        auth.logout(request)
        print("logout")
        return redirect("login")
