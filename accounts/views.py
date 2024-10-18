from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm

def registerView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.role = 'user'
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.POST.get('next') or reverse('home'))
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def profileView(request):
    return render(request, 'accounts/profile.html')

@login_required
def profileView_update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
                return redirect('profile')
            user.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'accounts/profile_update.html', {'form': form})