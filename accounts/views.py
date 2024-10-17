from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'user'
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

def custom_login(request):
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