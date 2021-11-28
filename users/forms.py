from django import forms


class ProfileForm(forms.Form):
    website = forms.URLField(max_length=200)
    biography = forms.CharField(max_length=500)
    picture = forms.ImageField()