from django import forms

from posts.models import Post
from users.models import User
from users.models import Profile

class SignupForm(forms.Form):

    username = forms.CharField(min_length=4, max_length=20)
    password = forms.CharField(max_length=80, widget=forms.PasswordInput())
    password_confirmation = forms.CharField(max_length=80, widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('Username is already in use.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user has already registered using this email')
        return email
    
    def clean(self):
        """Verify password confirmation match."""
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Passwords do not match')

        return data
    
    def save(self):
        """Create user and profile"""
        data = self.cleaned_data
        data.pop('password_confirmation')

        user = User.objects.create_user(**data)
        profile = Profile(user=user)
        profile.save()

class PostForm(forms.ModelForm):
    class Meta:

        model = Post
        fields = ('user', 'profile', 'title', 'photo')