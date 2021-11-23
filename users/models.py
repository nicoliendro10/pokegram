from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(blank=True)
    biography = models.TextField(blank=True)
    picture = models.ImageField(
        upload_to='users/pictures',
        blank=True,
        null=True
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
