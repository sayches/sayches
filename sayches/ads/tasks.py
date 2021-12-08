import datetime

from celery import shared_task
from subsections.models import Ads

from .models import CreateAds


@shared_task
def expired_ad():
    today = datetime.date.today()
    expired_ad = Ads.objects.filter(ad_end_date=today).filter(status="1")
    try:
        if expired_ad:
            expired_ad.update(status="5")
            CreateAds.objects.all().filter(end_date=today).delete()
    except:
        pass
