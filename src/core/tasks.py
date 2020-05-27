from celery import Celery
from celery.task import periodic_task
from celery.schedules import crontab
from rompas.models import Profile
from django.utils import timezone
from dateutil.relativedelta import relativedelta


@periodic_task(
    run_every=(crontab(hour='*/12', minute='0')),
    name="check_subscription",
    ignore_result=True
)
def check_subscription():
    profiles = Profile.objects.all()
    today = timezone.now()
    for profile in profiles:
        if profile.subscription_end:
            if profile.subscription_end < today:
                profile.subscription_active = False
                if profile.tokens_end:
                    if profile.tokens_end < today:
                        profile.tokens_left = 0
                else:
                    profile.tokens_end = today + relativedelta(months=3)
                profile.save()
