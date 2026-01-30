from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login")
def home_view(request):
    return render(request, "home.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.groups.filter(name="Администратор").exists():
                return render(request, "admin.html")
            if user.groups.filter(name="Авторизованный клиент").exists():
                return render(request, "client.html")
            if user.groups.filter(name="Менеджер").exists():
                return render(request, "manager.html")
        else:
            return render(request, "login.html", {"error": "Неправильный логин или пароль"})
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("/login")