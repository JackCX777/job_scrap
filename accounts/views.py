from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
import datetime as dt

from accounts.forms import UserLoginForm, UserRegistrationForm, UserPreferenceForm, ContactForm
from scrap.models import Error

User = get_user_model()

def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        messages.success(request, 'Пользователь добавлен в систему.')
        return render(request, 'accounts/register_done.html', {'new_user': new_user})
    return render(request, 'accounts/register.html', {'form': form})


def user_preference_view(request):
    contact_form = ContactForm()
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserPreferenceForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.programming_language = data['programming_language']
                user.send_email = data['send_email']
                user.save()
                messages.success(request, 'Настройки сохранены.')
                return redirect('accounts:user_preference')
        form = UserPreferenceForm(
            initial={
                'city': user.city,
                'programming_language': user.programming_language,
                'send_email': user.send_email
            }
                                  )
        return render(request, 'accounts/user_preference.html', {'form': form, 'contact_form': contact_form})
    else:
        return redirect('accounts:login')


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            query_set = User.objects.get(pk=user.pk)
            query_set.delete()
            messages.error(request, 'Пользователь удален из системы.')
    return redirect('home')


def contact_view(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST or None)
        if contact_form.is_valid():
            data = contact_form.cleaned_data
            city = data.get('city')
            programming_language = data.get('programming_language')
            email = data.get('email')
            query_set_er = Error.objects.filter(timestamp=dt.datetime.today())
            if query_set_er.exists():
                error = query_set_er.first()
                data = error.data.get('user_data', [])
                data.append({'city': city, 'programming_language': programming_language, 'email': email})
                error.data['user_data'] = data
                error.save()
            else:
                data = [{'city': city, 'programming_language': programming_language, 'email': email}]
                Error(data=f'user_data: {data}').save()
                messages.success(request, 'Данные отправлены администрации.')
                return redirect('accounts:user_preference')
        else:
            return redirect('accounts:user_preference')
    else:
        redirect('accounts:login')