from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderStatus(models.IntegerChoices):
    OPENED = 1, _('Opened')
    EXECUTED = 2, _('Executed')
    BILLED = 3, _('Billed')
