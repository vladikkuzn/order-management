from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.IntegerChoices):
    SALES_CONSULTANT = 1, _('Sales consultant')
    CASHIER = 2, _('Cashier')
    ACCOUNTANT = 3, _('Accountant')

    __empty__ = _('(Unknown)')
