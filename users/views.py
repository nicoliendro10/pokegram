from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from users.forms import ProfileForm
from posts.forms import SignupForm



def login_view(request):
    if request.user.is_authenticated:
	    return redirect('posts:feed')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('posts:feed')
        else:
            error_message = {
                'error' : 'Invalid username or password'
            }
            return render(request, 'users/login.html', error_message)
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    import pdb; pdb.set_trace()
    logout(request)
    return redirect('users:login')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    print("Form:")
    print(form)
    return render(
        request=request,
        template_name='users/signup.html',
        context={'form': form}
    )


@login_required
def update_profile(request):
    import pdb; pdb.set_trace()
    profile = request.user.profile
    print(profile)
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