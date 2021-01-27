from django.contrib.auth.models import User
from django.db import models
from civilopedia.models import Token


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.OneToOneField(Token, null=True, on_delete=models.DO_NOTHING)

