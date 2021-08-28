import datetime

from celery import shared_task
from django.db.models import DurationField, F, ExpressionWrapper
from django.utils import timezone

from orders_app.models import Product


@shared_task
def set_discounts():
    Product.objects.annotate(
        diff=ExpressionWrapper(timezone.now() - F('created_at'), output_field=DurationField())
    ).filter(
        diff__gte=datetime.timedelta(weeks=4)
    ).update(discount=20)
