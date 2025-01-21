from celery import shared_task
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import User


@shared_task
def deactivate_inactive_users():
    one_month_ago = now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    count = inactive_users.update(is_active=False)
