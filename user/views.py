from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from event.models import EventRegistration
from .forms import LoginForm, ProfileRegistrationForm, ProfileEditForm

# Представление для входа пользователя в систему
@ensure_csrf_cookie
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Попытка аутентификации пользователя
            user = authenticate(request, email=cd.get('email'), password=cd.get('password'))
            if user is not None:
                if user.is_active:
                    # Если пользователь активен, выполняется вход в систему
                    login(request, user)
                    return redirect('dashboard') # Перенаправление на панель управления
                else:
                    # Если аккаунт отключен, возвращается сообщение
                    return HttpResponse('Аккаунт отключен')
            else:
                # Если аутентификация не удалась, возвращается сообщение
                return HttpResponse('Неверный логин или пароль')
    else:
        # Если запрос не POST, создается пустая форма для входа
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

# Представление для отображения панели управления (требует аутентификации)
@login_required
def dashboard(request):
    return render(request,
                  'user/dashboard.html',
                  {'section': 'dashboard'})

# Регистрация нового пользователя
def register(request):
    if request.method == 'POST':
        profile_form = ProfileRegistrationForm(request.POST)
        if profile_form.is_valid():
            # Создание нового пользователя и установка пароля
            new_profile = profile_form.save(commit=False)
            new_profile.set_password(profile_form.cleaned_data['password'])
            new_profile.save()
            # Аутентификация и вход в систему нового пользователя
            user = authenticate(request, email=new_profile.email, password=profile_form.cleaned_data['password'])
            login(request, user)
            return render(request,
                          'user/register_done.html',
                          {'new_profile': new_profile})
    else:
        # Если запрос не POST, создается пустая форма регистрации
        profile_form = ProfileRegistrationForm()
    return render(request,
                  'user/register.html',
                  {'profile_form': profile_form})

# Редактирование профиля пользователя (требует аутентификации)
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        # Если запрос не POST, создается форма для редактирования профиля
        form = ProfileEditForm(instance=request.user)
    return render(request, 'user/edit_profile.html', {'form': form})

@login_required
def dashboard(request):
    registered_events = EventRegistration.objects.filter(user=request.user).order_by('event__start_time')
    return render(request,
                  'user/dashboard.html',
                  {'section': 'dashboard', 'registered_events': registered_events})
@login_required
def user_logout(request):
    logout(request)
    return render(request, 'registration/logged_out.html', {})