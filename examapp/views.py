from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Product
import logging
from django.contrib import messages
from django.core.exceptions import PermissionDenied
logger = logging.getLogger(__name__)


def check_group_access(user, group_name):
    if not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()

def home_view(request):
    try:
        products = Product.objects.all()
        return render(request, "home.html", {'products': products})
    except Exception as e:
        logger.error(f"Ошибка при загрузке главной страницы: {str(e)}")
        messages.error(request, "Произошла ошибка при загрузке данных. Пожалуйста, попробуйте позже.")
        return render(request, "home.html", {'products': []})

@login_required
def client(request):
    if request.session.get('show_welcome_message'):
        username = request.session.get('username', '')
        messages.success(request, f"Добро пожаловать, {username}!")
    if not check_group_access(request.user, "Авторизованный клиент"):
        messages.error(request,
                       "У вас нет доступа к этой странице. "
                       "Требуется роль 'Авторизованный клиент'.")
        raise PermissionDenied("Доступ запрещен")

    try:
        products = Product.objects.all()
        return render(request, "client.html", {'products': products})
    except Exception as e:
        logger.error(f"Ошибка при загрузке страницы клиента: {str(e)}")
        messages.error(request, "Произошла ошибка при загрузке данных.")
        return render(request, "client.html", {'products': []})

@login_required
def manager(request):
    if request.session.get('show_welcome_message'):
        username = request.session.get('username', '')
        messages.success(request, f"Добро пожаловать, {username}!")
    products = Product.objects.all()
    return render(request, "manager.html", {'products': products})

@login_required
def admin(request):
    if request.session.get('show_welcome_message'):
        username = request.session.get('username', '')
        messages.success(request, f"Добро пожаловать, {username}!")
    products = Product.objects.all()
    return render(request, "admin.html", {'products': products})

def login_view(request):
    if request.session.get('show_logout_message'):
        username = request.session.get('username', '')
        if username:
            messages.info(request, f"До свидания, {username}! Вы успешно вышли из системы.")
        else:
            messages.info(request, "Вы успешно вышли из системы.")
        del request.session['show_logout_message']
        if 'username' in request.session:
            del request.session['username']
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username:
            messages.error(request,
                           "Поле 'Логин' не может быть пустым. "
                           "Пожалуйста, введите ваш логин.")
            return render(request, "login.html", {'username': username})

        if not password:
            messages.error(request,
                           "Поле 'Пароль' не может быть пустым. "
                           "Пожалуйста, введите ваш пароль.")
            return render(request, "login.html", {'username': username})

        if len(password) < 8:
            messages.warning(request,
                             "Введенный пароль слишком короткий. "
                             "Минимальная длина пароля - 8 символов.")
            return render(request, "login.html", {'username': username})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if hasattr(user, 'profile') and user.profile.is_blocked:
                logout(request)
                messages.error(request,
                               "Ваша учетная запись временно заблокирована. "
                               "Пожалуйста, обратитесь к администратору.")
                return redirect('login')

            request.session['show_welcome_message'] = True
            request.session['username'] = user.get_full_name() or user.username
            logger.info(f"Пользователь {username} успешно вошел в систему")

            if check_group_access(user, "Администратор"):
                return redirect('admin')
            elif check_group_access(user, "Авторизованный клиент"):
                return redirect('client')
            elif check_group_access(user, "Менеджер"):
                return redirect('manager')
            else:
                messages.warning(request,
                                 "У вашей учетной записи не назначено ни одной роли. "
                                 "Обратитесь к администратору для назначения прав доступа.")
                return redirect('home')
        else:
            messages.error(request,
                           "Неверное имя пользователя или пароль. "
                           "Пожалуйста, проверьте введенные данные и попробуйте снова. "
                           "Если вы забыли пароль, обратитесь к администратору.")
    return render(request, "login.html")

def logout_view(request):
    if request.user.is_authenticated:
        username = request.user.get_full_name() or request.user.username
        request.session['show_logout_message'] = True
        request.session['username'] = username
        logger.info(f"Пользователь {username} вышел из системы")
    logout(request)
    return redirect("/")