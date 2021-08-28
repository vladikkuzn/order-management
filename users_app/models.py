from django.db import models
from django.contrib.auth.models import AbstractUser

from users_app.enums import Role


class User(AbstractUser):
    role = models.PositiveSmallIntegerField(choices=Role.choices, null=True)
    # You can create Role model separately and add ManyToMany if user has more than one role
