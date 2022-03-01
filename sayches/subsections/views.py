import re
import uuid
from django.core.mail import send_mail
import environ
import requests
from ads.models import AdsPricing
from ads.views import targeted_ads, voucher_discount, ad_period, validate_voucher
from coinbase.wallet.client import Client
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_GET
from message.models import SaychesMessage
from posts.models import Post, Hashtag
from posts.models import PostsTimestamp
from posts.utils import get_parsed_meta_url
from subsections.models import Ads, PAYMENT_METHOD
from users.models import BlacklistUser, FromSayches
from users.models import User
from ads.models import CreateAds
from .forms import flair_form_public, AdsStepOneForm, AdsStepTwoForm, AdsStepFourVoucherForm, HelpForm
from .models import Doc, News

env = environ.Env()


@require_GET
def docs(request):
    doc = Doc.objects.all().order_by("name")
    context = {'other_docs': doc}
    return render(request, 'docs/docs.html', context)


@require_GET
def single_docs(request, slug):
    doc = Doc.objects.all().order_by("name")
    single_doc = get_object_or_404(Doc, slug=slug)
    context = {'single_doc': single_doc, 'other_docs': doc}
    return render(request, 'docs/docs.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def help(request):
    help_form = HelpForm(initial={"user": request.user})
    message = ''
    if request.method == "POST":
        help_form = HelpForm(request.POST, initial={'user': request.user})
        if help_form.is_valid():
            new_report = help_form.save(commit=False)
            new_report.reference_number = str(uuid.uuid4())[:12].upper()
            new_report.save()
            message = 'We will get back to you soon.'
            admin_email_body = 'Hey Admin, A new ticket has been opened by a user.'
            send_mail('Sayches | New Ticket Opened', admin_email_body, settings.DEFAULT_FROM_EMAIL,
                        [settings.DEFAULT_FROM_EMAIL])
            render_body = 'We have received your inquiry and will get back to you soon.'
            if request.user.is_authenticated:
                FromSayches.from_sayches(title='Help #{0}'.format(new_report.reference_number),
                                            message=render_body, to=request.user)

            help_form = HelpForm(initial={"user": request.user, "message": message})
    return render(request, 'help/help.html', context={
        'message': message,
        "help_form": help_form,
    })


@require_GET
def newsroom(request):
    search = request.GET.get('q')
    if search:
        default = search
        news = News.objects.filter(Q(article_title__icontains=search) | Q(article_content__icontains=search)).order_by(
            '-id')
    else:
        default = ''
        news = News.objects.all().order_by('-publish_date')
    paginator = Paginator(news, 5)
    page_number = request.GET.get('p', 1)
    try:
        page_obj = paginator.get_page(page_number)
        news = paginator.page(int(page_number))
    except EmptyPage:
        page_obj = paginator.get_page(1)
        news = paginator.page(int(1))

    context = {'news': news, 'page_obj': page_obj, 'default': default}
    return render(request, 'newsroom/newsroom.html', context)


def first_post(request):
    user = request.user
    if user.first_post == False:
        if PostsTimestamp.objects.filter(user=user).count() >= 1:
            message = "First post 👏\nYou should keep doing that! 😉"
            SaychesMessage.objects.create(message=message).user.set([request.user])
            user.first_post = True
            user.save()
    return first_post


def lost_virginity(request):
    user = request.user
    if user.lost_virginity == False:
        if user.profile.photo and user.first_post and not user.first_login and User.user_profile_age(
                request.user) > '0 days':
            message = "Yay! You lost your Sayches virginity! 😊"
            SaychesMessage.objects.create(message=message).user.set([request.user])
            user.lost_virginity = True
            user.save()
    return lost_virginity


@require_GET
def article(request, slug):
    news = get_object_or_404(News, slug=slug)
    cleantext = re.sub(re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});'), '', news.article_content)
    meta_tag_desp = cleantext[0:160]
    context = {'news': news, 'meta_tag_desp': meta_tag_desp}
    return render(request, 'newsroom/article.html', context)


@require_http_methods(["GET", "POST"])
def home(request):
    form = flair_form_public(request.POST)
    posts = Post.objects.all()

    if request.user.is_authenticated:
        random_user_list = User.objects.filter(
            country=request.user.country
            ).exclude(user_hash=request.user.user_hash
            ).exclude(is_superuser=True).order_by(
            '?')[:3]
    else:
        random_user_list = User.objects.exclude(is_superuser=True).order_by('?')[:3]
    hashtags = Hashtag.objects.all()[:3]

    if request.user.is_authenticated:
        ad = targeted_ads(request)
    else:
        ad = CreateAds.objects.order_by('?').first()
    try:
        Ads.ad_impressions(ad)
    except:
        pass

    if request.user.is_authenticated:
        is_block_post = BlacklistUser.objects.filter(user=request.user, on_post=True).exists()
    else:
        is_block_post = None

    if request.user.is_authenticated:
        is_search_user_profile = BlacklistUser.objects.filter(Q(user=request.user),
                                                                Q(on_post=True) | Q(on_login=True) | Q(
                                                                    on_message=True)).exists()
    else:
        is_search_user_profile = None


    all_blocked_user = BlacklistUser.objects.filter(on_login=True).distinct()

    if request.user.is_authenticated:
        first_post(request)
        lost_virginity(request)
    else:
        pass

    try:
        ad_slug = Ads.objects.get(slug=ad.ad_id)
    except:
        ad_slug = None

    context = {
        "ad": ad,
        "is_search_user_profile": is_search_user_profile,
        "users": random_user_list,
        "all_blocked_user": all_blocked_user,
        "hashtags": hashtags,
        "posts": posts,
        "form": form,
        "ad_slug": ad_slug,
        "is_block_post": is_block_post}

    return render(request, 'feed/feed.html', context)


@require_GET
def remove_alert(request):
    if 'rate_limiter_comment' in request.session:
        if request.session['rate_limiter_comment'] == True:
            request.session['rate_limiter_comment'] = False

    if 'rate_limiter_post' in request.session:
        if request.session['rate_limiter_post'] == True:
            request.session['rate_limiter_post'] = False

    return HttpResponseRedirect(get_parsed_meta_url(request, "/", ))


@login_required
@require_http_methods(["GET", "POST"])
def ads_step_one(request):
    if request.user.disposable:
        return redirect(reverse('subsections:home'))
    else:
        form = AdsStepOneForm(initial={'user': request.user})
        if request.method == 'POST':
            form = AdsStepOneForm(request.POST, initial={'user': request.user})
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
                return redirect(reverse('subsections:ads-step-two', kwargs={"ads_slug": obj.slug}))
        context = {"form": form, }
    return render(request, 'ads/form/step_one.html/', context)


@login_required
@require_http_methods(["GET", "POST"])
def ads_step_two(request, ads_slug):
    try:
        ads = Ads.objects.get(slug=ads_slug)
    except:
        return redirect(reverse('subsections:home'))
    if ads.ad_headline:
        return redirect(reverse('subsections:ads-step-three', kwargs={"ads_slug": ads_slug}))
    if ads.user != request.user:
        return redirect(reverse('subsections:home'))
    form = AdsStepTwoForm()
    if request.method == 'POST':
        form = AdsStepTwoForm(request.POST, request.FILES, instance=ads)
        if form.is_valid():
            if ad_period(ads) > 0:
                obj = form.save(commit=False)
                obj.save()
                form.save_m2m()
                return redirect(reverse('subsections:ads-step-three', kwargs={"ads_slug": ads_slug}))
    context = {"form": form, "ads_slug": ads_slug}
    return render(request, 'ads/form/step_two.html/', context)


@login_required
@require_http_methods(["GET", "POST"])
def ads_step_three(request, ads_slug):
    try:
        ads = Ads.objects.get(slug=ads_slug)
    except:
        return redirect(reverse('subsections:home'))
    if request.method == 'POST':
        ads_pricing_id = request.POST.get("ads_pricing_id", None)
        ads_pricing = AdsPricing.objects.get(id=ads_pricing_id)
        if not ads.ad_plan:
            ads.ad_plan = ads_pricing
            ads.save()
            ads.ad_price = ad_period(ads) * ads_pricing.price
            ads.save()
        return redirect(reverse('subsections:ads-step-four', kwargs={"ads_slug": ads_slug}))
    else:
        if ads.ad_plan:
            return redirect(reverse('users:profile_update'))
        if ads.user != request.user:
            return redirect(reverse('subsections:home'))
        ad_plan = AdsPricing.objects.all()
        context = {
            "ads_pricing": ad_plan,
            "ads_slug": ads_slug,
        }

        return render(request, 'ads/form/step_three.html/', context)


def get_bitcoin_address():
    try:
        client = Client(env("COINBASE_API_KEY"),
                        env("COINBASE_API_SECRET"),
                        api_version=env("COINBASE_API_VERSION"))
        primary_account = client.get_primary_account()
        bitcoin_address = primary_account.create_address()['address']
    except:
        bitcoin_address = None
        pass
    return bitcoin_address


@login_required
@require_http_methods(["GET", "POST"])
def ads_step_four(request, ads_slug):
    payment_method = PAYMENT_METHOD

    exchange_response = requests.get(settings.COINBASE_EXCHANGE_RATES_API).json()
    BTC_GBP = exchange_response['data']['rates']['GBP']

    try:
        ads = Ads.objects.get(slug=ads_slug)
    except:
        return redirect(reverse('subsections:home'))

    if ads.to_bitcoin_address is None:
        bitcoin_address = get_bitcoin_address()
        ads.to_bitcoin_address = bitcoin_address
        ads.save()
    else:
        bitcoin_address = ads.to_bitcoin_address

    if request.method == 'POST':
        if ads.voucher_code:
            ads.voucher_code.expired = True
            ads.voucher_code.save()
            voucher_discount(ads.voucher_code, ads)
        else:
            ads.amount_due = ads.ad_price
        ads.save()
        body = 'Your ad has been received, you do not need to do anything now, you can follow the status of your ad in Settings > Ads History. The advertisement will be reviewed by the Sayches team as soon as possible to verify your business and that the advertisement complies with the terms and conditions.'
        FromSayches.from_sayches(title='Ad Status: Pending', message=body, to=ads.user)
        admin_email_body = 'Hey Admin, There is a new ad request.'
        send_mail('Ad Request', admin_email_body, settings.DEFAULT_FROM_EMAIL,
                  [settings.DEFAULT_FROM_EMAIL])
        return redirect(reverse('users:profile_update'))

    elif request.method == 'GET':
        if ads.user != request.user:
            return redirect(reverse('subsections:home'))

        voucher_code = request.GET.get('voucher')
        discount_percentage = 0
        amount_due = ads.ad_price
        btc_amount = amount_due / float(BTC_GBP)

        try:
            ad = Ads.objects.get(slug=ads_slug)
            ad_plan = ad.ad_plan
        except:
            ad_plan = None

        voucher_form = AdsStepFourVoucherForm()
        voucher = validate_voucher(voucher_code, request.user, ad_plan)
        if voucher:
            ads.voucher_code = voucher
            voucher_discount_func = voucher_discount(voucher, ads)
            discount_percentage = voucher_discount_func[0]
            amount_due = voucher_discount_func[1]
            btc_amount = amount_due / float(BTC_GBP)
            ads.save()
            voucher_form = AdsStepFourVoucherForm(initial={'disable': True, 'voucher': voucher_code})

        try:
            Ads.objects.filter(slug=ads_slug).update(btc_amount_due=btc_amount)
        except:
            pass

        context = {
            "ads_slug": ads_slug,
            "ad_price": ads.ad_plan.price,
            "plan": ads.ad_plan.title,
            "start_date": ads.ad_start_date,
            "end_date": ads.ad_end_date,
            "total_amount": ads.ad_price,
            "days": ad_period(ads),
            "voucher_form": voucher_form,
            "discount_percentage": discount_percentage,
            "amount_due": amount_due,
            "invalid_voucher": voucher == False,
            "payment_method": payment_method,
            "btc_amount": btc_amount,
            "bitcoin_address": bitcoin_address,
        }
        return render(request, 'ads/form/step_four.html/', context)
