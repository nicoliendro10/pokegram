from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls.base import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import DetailView, FormView
from django.urls import reverse

from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView

from posts.forms import SignupForm
from posts.models import Post
from users.models import Profile

class UserDetailView(LoginRequiredMixin, DetailView):

    template_name = 'users/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(user=user).order_by('-created')
        return context
        

class LoginView(auth_views.LoginView):

    template_name = 'users/login.html'
    redirect_authenticated_user = True

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):

    template_name = 'users/logged_out.html'

@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')

class SignupView(FormView):

    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class UpdateProfileView(LoginRequiredMixin, UpdateView):

    template_name = 'users/profile.html'
    model = Profile
    fields = ['website', 'biography', 'picture']

    def get_object(self):
        return self.request.user.profile
    
    def get_success_url(self):
        username = self.object.user.username
        return reverse('users:detail', kwargs={'username': username})