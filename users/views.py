from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from users.models import Profile
from users.forms import ProfileForm

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

@login_required
def update_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            profile.website = data['website']
            profile.biography = data['biography']
            profile.picture = data['picture']
            profile.save()

            message = 'Your profile has been updated'
            messages.success(request, message)
            
            return redirect('profile')
    else:
        form = ProfileForm()

    return render(
        request=request, 
        template_name='users/profile.html',
        context={
            'profile': profile,
            'user': request.user,
            'form': form
        }
    )