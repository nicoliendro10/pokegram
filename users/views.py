from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import Profile

from django.db.utils import IntegrityError

def login_view(request):
    if request.user.is_authenticated:
	    return redirect('feed')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('feed')
        else:
            error_message = {
                'error' : 'Invalid username or password'
            }
            return render(request, 'users/login.html', error_message)
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']
        if password != password_confirmation:
            message_error = {
                'error': 'Password and password confirmation does not match'
            }
            return render(request, 'users/signup.html', message_error)
        try:
            user = User.objects.create_user(username=username, password=password)
            if User.objects.filter(email=user.email):
                return render(request, 'users/signup.html', {'error': 'Email is already in used!'})
        except IntegrityError:
            message_error = {
                'error': 'Username is already taken'
            }
            return render(request, 'users/signup.html', message_error)
        user.email = email
        user.save()

        profile = Profile(user=user)
        profile.save()
        return redirect('login')
    return render(request, 'users/signup.html')