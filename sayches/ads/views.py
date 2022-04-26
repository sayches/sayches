import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from subsections.models import Ads

from .models import CreateAds, Vouchers


def targeted_ads(request):
    ad = CreateAds.objects.filter(Q(location=request.user.country) |
                                  Q(target_all_users=True) |
                                  Q(target_user_list=request.user)).order_by('?').first()
    return ad


@login_required
def ad_invoice(request, invoice_number):
    ads = Ads.objects.get(slug=invoice_number)
    try:
        ads_owner = Ads.objects.get(user=request.user)
    except:
        ads_owner = None
    if request.user != ads.user:
        return redirect('subsections:home')
    context = {
        "ads": ads,
        "ads_owner": ads_owner,
    }
    return render(request, 'ads/invoice.html', context)


def voucher_discount(voucher, ads):
    discount_percentage = voucher.discount_percentage
    discount_amount = discount_percentage / 100 * ads.ad_price
    amount_due = ads.ad_price - discount_amount
    ads.amount_due = amount_due
    ads.discount_amount = discount_amount
    ads.discount = discount_percentage
    ads.save()
    return discount_percentage, amount_due


def ad_period(ads):
    start_date = ads.ad_start_date
    end_date = ads.ad_end_date
    number_of_days = (end_date - start_date).days
    return number_of_days


def ad_clicks(request, slug):
    if request.is_ajax():
        try:
            ad = Ads.objects.get(status="1", slug=slug)
            ad.clicks.add(request.user)
            ad.save()
        except:
            return JsonResponse({'success': 'false'})
        return JsonResponse({'success': 'true'})
    return HttpResponseBadRequest()


def validate_voucher(voucher_code, user, ad_plan):
    if not voucher_code:
        return
    vouchers = Vouchers.objects.filter(voucher_code=voucher_code, expired=False)

    if not vouchers.exists():
        return False

    voucher = vouchers.first()
    try:
        if voucher.end_date <= datetime.date.today():
            vouchers.update(expired=True)
    except:
        pass

    if voucher.is_expired or not voucher.is_valid(user, ad_plan):
        return False

    return voucher
