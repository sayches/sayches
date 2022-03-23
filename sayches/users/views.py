import json
from datetime import datetime

from ads.models import AdminNotifications
from ads.models import AdsOwners
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.views.generic import TemplateView
from message.models import Chat
from posts.models import Post, Hashtag
from posts.models import PostsTimestamp, Mentions, Likes, ReportPost
from posts.utils import posts_to_json, get_parsed_meta_url, replace_profanity_words
from rest_framework.authtoken.models import Token
from subsections.forms import flair_form_public
from subsections.models import Ads
from subsections.models import Help
from users.models import Activity
from users.models import BlacklistUser
from users.models import FromSayches
from users.models import User
from users.utils import create_action
from users.utils import log_deleted_user
from utils.export_csv import export_ads_history

from .forms import EditProfileForm, UserVerificationForm
from .models import Profile, Bell, PingPong, ReportUser, UserVerification, UserRSA

profile_name_var = 'users:profile_name'


@require_GET
def forget_user(request, username):
    try:
        user = request.user
        user.is_active = False
        user.save()
        log_deleted_user(user)
        User.objects.filter(username=request.user).delete()
        Profile.objects.filter(user=user)
    except User.DoesNotExist:
        pass

    return redirect('/')


@require_http_methods(["GET", "POST"])
def profile_detail(request, id):
    form = flair_form_public(request.POST)
    profile = get_object_or_404(Profile, id=id)
    user = get_object_or_404(User, profile=profile)
    user_follow = User.objects.all()[0:1]

    sort_type = request.GET.get('sortby', None)

    if request.user == profile.user:
        if sort_type == "oldest":
            posts = Post.objects.filter(user=user).order_by('-pinned_post', 'created_at')
        else:
            posts = Post.objects.filter(user=user).order_by('-pinned_post', '-created_at')
    else:
        if sort_type == "oldest":
            posts = Post.objects.filter(user=user).order_by('created_at')
        else:
            posts = Post.objects.filter(user=user).order_by('-created_at')

    for post in posts:
        post.created_at = timezone.localtime(post.created_at)
        post.save()
    hashtags = Hashtag.objects.all()[:3]
    if request.is_ajax():
        data = format_post_with_paginator(request, user, posts)
        return JsonResponse(data, safe=False)

    check_user_report = ReportUser.objects.filter(user_reporter=request.user, user=user).first()
    context = {
        'check_user_report': check_user_report,
        'profile': profile,
        "user_follow": user_follow,
        'user': user, 'posts': posts,
        'hashtags': hashtags,
        "form": form,
    }

    return render(request, 'profile/profile.html', context)


@require_GET
def format_post_with_paginator(request, user, posts):
    data = posts_to_json(request, user, posts)
    paginator = Paginator(data, 10)
    page_number = request.GET.get('page', 1)
    try:
        page_data = paginator.page(page_number)
        data = page_data.object_list
    except EmptyPage:
        data = []
    return data


def last_post_timestamp(user):
    last_post_time = PostsTimestamp.objects.filter(user=user)
    if last_post_time:
        last_post_time = last_post_time.last().post_timestamp
    else:
        last_post_time = "ROTTING FISH 💀⚰️🎣"
    return last_post_time


def directory(request):
    user = User.objects.filter(lost_virginity=True).exclude(is_superuser=True)
    
    paginator = Paginator(user, 20)
    page_number = request.GET.get('p', 1)
    try:
        page_obj = paginator.get_page(page_number)
        page_data = paginator.page(page_number)
        user = page_data.object_list
    except EmptyPage:
        page_obj = paginator.get_page(1)
        user = []
    context = {
        'user': user,
        'page_obj': page_obj,
    }
    return render(request, 'account/directory.html', context)


def user_birthday(user):
    profile = get_object_or_404(Profile, user=user)
    datetime_now = timezone.now()
    user_birthday_flag = False
    now_day, now_month = datetime_now.day, datetime_now.month
    if profile.created_at:
        if profile.created_at.month == now_month and profile.created_at.day == now_day:
            user_birthday_flag = True
    return user_birthday_flag


@login_required
def export_my_data(request, username):
    if request.user.username == username:
        user_obj = request.user
        rsa_obj = UserRSA.objects.filter(user=request.user).values_list("public_pem", flat=True)
        bell_obj = Bell.objects.filter(user=request.user)
        verification_obj = UserVerification.objects.filter(user=request.user).values_list("verified", flat=True)
        report_user_obj = ReportUser.objects.filter(user_reporter=request.user).values_list("user_reporter",
                                                                                            flat=True).count()
        notification_sender_obj = Activity.objects.filter(sender=request.user).count()
        notification_receiver_obj = Activity.objects.filter(receiver=request.user).count()
        post_timestamp_obj = PostsTimestamp.objects.filter(user=request.user).count()
        hashtag_obj = Hashtag.objects.filter(author=request.user).count()
        mention_obj = Mentions.objects.filter(posts__user=request.user).count()
        mention_obj = Mentions.objects.filter(posts__user=request.user).count()
        reaction_obj = Likes.objects.filter(user=request.user).count()
        report_post_obj = ReportPost.objects.filter(post_reporter=request.user).count()
        private_key = request.session['private_pem']
        token_obj = Token.objects.filter(user=request.user).first()
        ad_obj = Ads.objects.filter(user=request.user).count()
        chat_obj = Chat.objects.filter(members=request.user).count()
        help_obj = Help.objects.filter(username=request.user)
        business_obj = AdsOwners.objects.filter(user=request.user)

        context = {
            "user_obj": user_obj,
            "rsa_obj": rsa_obj,
            "bell_obj": bell_obj,
            "verification_obj": verification_obj,
            "report_user_obj": report_user_obj,
            "notification_sender_obj": notification_sender_obj,
            "notification_receiver_obj": notification_receiver_obj,
            "post_timestamp_obj": post_timestamp_obj,
            "hashtag_obj": hashtag_obj,
            "mention_obj": mention_obj,
            "reaction_obj": reaction_obj,
            "report_post_obj": report_post_obj,
            "private_key": private_key,
            "token_obj": token_obj,
            "ad_obj": ad_obj, "business_obj": business_obj,
            "chat_obj": chat_obj, "help_obj": help_obj,
        }
        return render(request, 'settings/account_data.html', context)
    else:
        return redirect(reverse('subsections:home'))


@require_http_methods(["GET", "POST"])
def profile_detail_name(request, username):
    current_user = None
    user = get_object_or_404(User, user_hash__iexact=username)
    user_birthday_flag = user_birthday(user)

    if request.user.is_authenticated:
        current_user = request.user
        last_post_time = last_post_timestamp(request.user)

    form = flair_form_public(request.POST)
    user_following = []
    user_followers = []
    other_user_following = []
    other_user_followers = []
    following_request_user = []
    today_ping = False

    if request.user.is_authenticated:
        today_ping = PingPong.objects.filter(pinger_user=request.user, pinged_user=user,
                                             created_at__date=timezone.now().date()).exists()
    posts = Post.valid.filter(user=user)

    user = get_object_or_404(User, user_hash__iexact=username)

    last_post_time = last_post_timestamp(user)

    posts = Post.valid.filter(user=user)
    hashtags = Hashtag.objects.all()
    if request.is_ajax():
        data = posts_to_json(request, user, posts)
        return JsonResponse(data, safe=False)

    belled = False
    if request.user.is_authenticated:
        bells_users_ids = user.ring_from.values_list('user').first()
        if bells_users_ids and request.user.id in bells_users_ids:
            belled = True

    user.user_profile_age()

    if UserVerification.objects.filter(user=user).exists():
        verification = UserVerification.objects.filter(user=user).values_list("verification", flat=True)[0]
    else:
        verification = None
    user_verification_form = UserVerificationForm({"verification": verification})

    check_post_black_list = BlacklistUser.objects.filter(user=user, on_post=True).first()
    is_block_post = False
    if check_post_black_list:
        is_block_post = True

    is_login_block = BlacklistUser.objects.filter(user=user, on_login=True).first()

    check_message_block_list = BlacklistUser.objects.filter(user=user, on_message=True).first()
    is_message_block = False
    if check_message_block_list:
        is_message_block = True

    check_over_all_block = BlacklistUser.objects.filter(Q(user=user),
                                                        Q(on_post=True) | Q(on_login=True) | Q(on_message=True)).first()
    is_search_user_profile = False
    if check_over_all_block:
        is_search_user_profile = True

    check_user_report = None
    if request.user.is_authenticated:
        check_user_report = ReportUser.objects.filter(user_reporter=request.user, user=user).first()

    context = {
        'last_post_time': last_post_time,
        'user_birthday_flag': user_birthday_flag,
        'check_user_report': check_user_report,
        "is_search_user_profile": is_search_user_profile,
        "is_block_post": is_block_post,
        "is_login_block": is_login_block,
        "is_message_block": is_message_block,
        'profile': user.profile, "user_following": user_following, "user_followers": user_followers,
        "other_user_followers": other_user_followers, "other_user_following": other_user_following,
        "following_request_user": following_request_user, 'user': user, 'posts': posts,
        'hashtags': hashtags, 'form': form, "belled": belled,
        'today_ping': today_ping,
        'user_verification_form': user_verification_form,
        "current_user": current_user,
        "user_total_posts": PostsTimestamp.objects.filter(user=user).count(),
        "user_current_posts": Post.objects.filter(user=user).count(),
    }

    return render(request, 'profile/profile.html', context)


from django.urls import reverse


def ads_history_pagination(request, obj_list):
    page = 10
    paginator = Paginator(obj_list, page)
    try:
        obj_list = paginator.page(request.GET.get('ads'))
    except PageNotAnInteger:
        obj_list = paginator.page(1)
    except EmptyPage:
        obj_list = paginator.page(paginator.num_pages)
    return obj_list


@login_required
@require_http_methods(["GET", "POST"])
def profile_update(request):
    user = request.user
    profile = user.profile

    check_block_user = BlacklistUser.objects.filter(Q(user=user),
                                                    Q(on_post=True) | Q(on_login=True) | Q(on_message=True)).first()
    is_block_user = False
    if check_block_user:
        is_block_user = True

    initial_dict = {
        'is_block_user': is_block_user,
        'name': user.name,
        'user': user,
        'username': user.username,
        'bio': profile.bio,
        'website': profile.website,
        'pgp_fingerprint': profile.pgp_fingerprint,
        'btc_address': profile.btc_address,
        'country': user.country.name,
    }
    form = EditProfileForm(user=user, initial=initial_dict)

    if request.method == 'POST' and "update_profile_basic" in request.POST:
        form = EditProfileForm(user=user, data=request.POST, files=request.FILES, initial=initial_dict)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['img']:
                profile.photo = cd['img']
            profile.pgp_fingerprint = cd['pgp_fingerprint']
            profile.btc_address = cd['btc_address']
            profile.bio = replace_profanity_words(cd['bio'])
            profile.website = cd['website']
            profile.save()
            user.name = replace_profanity_words(cd['name'])
            user.username = cd['username']
            user.country = request.POST.get('edit-location')
            user.save()
        else:
            return render(request, 'settings/settings.html', locals())

    # Start User Verification #

    elif request.method == 'POST' and "profile_verification" in request.POST:
        user_verification_form = UserVerificationForm(data=request.POST, initial={"user": user})
        if user_verification_form.is_valid():
            user_verification_form.save()
            FromSayches.from_sayches(title='New verification request', message='There is a verification request.',
                                        to=User.objects.filter(is_superuser=True).last())
        else:
            user_verification_form = UserVerificationForm(initial={"user": user})
    user_verification = UserVerification.objects.filter(user=request.user).exists()
    user_verification_form = UserVerificationForm(initial={"user": user})
    verification_tag = UserVerification.objects.filter(user=user, verified=True)

    # End User Verification #

    # Start Ads History #

    ads = Ads.objects.filter(user=user).order_by('-created_at')
    if request.GET.get('export') == 'ads_history':
        return export_ads_history(request, ads)
    ads_history = ads_history_pagination(request, ads)

    # End Ads History #

    token = Token.objects.filter(user=request.user).first()

    from_sayches_obj = FromSayches.objects.filter(to=request.user).order_by('-created_at')[:10]

    context = {
        'user': user, 'profile': profile, 'form': form,
        'user_verification_form': user_verification_form,
        'disable_messages': profile.disable_messages,
        'disable_notifications': profile.disable_notifications,
        'disable_ping': profile.disable_ping,
        'is_block_user': is_block_user,
        'ads': ads,
        'ads_history': ads_history,
        "token": token,
        "user_verification": user_verification,
        "verification_tag": verification_tag,
        'from_sayches_obj': from_sayches_obj,
    }

    return render(request, 'settings/settings.html', context)


@login_required
@require_POST
def set_or_remove_bell_for_user(request, username):
    targeted_user = get_object_or_404(User, username=username)
    try:
        Bell.objects.get(user=request.user, targeted_user=targeted_user).delete()
        return JsonResponse({'message': False})
    except Bell.DoesNotExist:
        Bell.objects.create(user=request.user, targeted_user=targeted_user)
        return JsonResponse({'message': True})


@login_required
@require_GET
def get_qr_code(request):
    return render(request, 'base/header/qr_code.html')


@login_required
@require_POST
def ping_user(request, username):
    if request.is_ajax():
        pinged_user = get_object_or_404(User, username=username)
        if pinged_user == request.user:
            return JsonResponse({'message': 'You can not ping your self'})
        if PingPong.objects.filter(pinger_user=request.user, pinged_user=pinged_user,
                                   created_at__date=timezone.now().date()).exists():
            return JsonResponse({'message': "You can't ping more than once in a day."})
        ping = PingPong.objects.create(pinger_user=request.user, pinged_user=pinged_user)
        create_action(request.user, pinged_user, "pinged you", activity_type="ping", target=ping)
        return JsonResponse({'message': 'You pinged ' + pinged_user.username})
    return HttpResponseBadRequest()


@login_required
@require_POST
def pong_user(request, id):
    if request.is_ajax():
        ping = get_object_or_404(PingPong, pk=id)
        if ping and not ping.pong:
            ping.pong = True
            ping.pong_time = timezone.now()
            ping.save()
            create_action(ping.pinged_user, ping.pinger_user, "ponged you", activity_type="pong", target=ping)
            return JsonResponse({'message': 'You have pong successfully.'})
        return JsonResponse({'message': 'Already ponged.'})
    return HttpResponseBadRequest()


@require_POST
def report_user(request):
    url = get_parsed_meta_url(request, "/")
    if request.POST:
        reason = request.POST.get("reason")
        user = request.POST.get("user")
        user = get_object_or_404(User, username=user)
        report_post = ReportUser(user_reporter=request.user, user=user, complaint_date=datetime.now(),
                                 flagging_reason=reason)
        report_post.save()
        admin_email_body = 'Hey Admin, There is a report on an account.'
        FromSayches.from_sayches(title='User Reported', message=admin_email_body,
                                    to=User.objects.filter(is_superuser=True).last())
        render_body = render_to_string('profile/report_user_email.html',
                                       {'username': user.username, 'reason': reason})
        FromSayches.from_sayches(title='Complaint regarding your account / {0}'.format(user.username),
                                 message=render_body, to=user)
    return HttpResponseRedirect(url)


gloable_template_name = "404.html"


class UpdateTimeView(LoginRequiredMixin, TemplateView):
    template_name = gloable_template_name

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        profile_update_time = int(self.request.POST.get('profile_update_time', 24))
        user = self.request.user
        if user and profile_update_time in [24, 48, 72, 0]:
            user.profile_update_time = profile_update_time
            user.save()
        return render(self.request, self.template_name, context=context)


class AutoAccountDeleteTime(LoginRequiredMixin, TemplateView):
    template_name = gloable_template_name

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        auto_account_delete_time = int(self.request.POST.get('auto_account_delete_time', 12))
        user = self.request.user
        if user and auto_account_delete_time in [0, 1, 6, 12]:
            user.auto_account_delete_time = auto_account_delete_time
            user.save()
        return render(self.request, self.template_name, context=context)


class UpdateNickView(LoginRequiredMixin, TemplateView):
    template_name = gloable_template_name

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        nickname = self.request.POST.get('nickname', User.ANONYMOUS_USER).strip()
        user = self.request.user
        if user and nickname in [User.ANONYMOUS_USER, User.UNKNOWN_USER, User.UNIDENTIFIED_USER, User.NAMELESS]:
            user.alias = nickname
            user.save()
        return render(self.request, self.template_name, context=context)


class UpdateToggleView(LoginRequiredMixin, TemplateView):
    template_name = gloable_template_name

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        toggle_key = self.request.POST.get('toggleKey')
        toggle_value = json.loads(self.request.POST.get(toggle_key, 'false'))
        profile = self.request.user.profile
        setattr(profile, toggle_key, toggle_value)
        profile.save()
        return render(self.request, self.template_name, context=context)


def search_user(request):
    if request.is_ajax():
        username = request.GET.get('username', None)
        queryset = User.objects.all().exclude(is_superuser=True).filter(username__icontains=username)[:6]
        data = []
        for user in queryset:
            data.append({'username': user.username})
        return JsonResponse(data, safe=False)
    return HttpResponseBadRequest()


@require_GET
def notification_number(request):
    if request.is_ajax():
        nfs = Activity.objects.filter(receiver_id=request.user).filter(read=False)
        for nf in nfs:
            nf.count = 0
            nf.save()
        admin_nf_users = AdminNotifications.objects.filter(user=request.user).filter(read=False)
        for x in admin_nf_users:
            x.read = False
            x.save()
        return JsonResponse({'ok': 'ok'})
    else:
        return HttpResponseBadRequest()


@require_GET
def mark_all_read(request):
    if request.is_ajax():
        nfs = Activity.objects.filter(receiver_id=request.user)
        for nf in nfs:
            nf.read = True
            nf.save()
        admin_nf_users = AdminNotifications.objects.filter(user=request.user)
        for admin_notify in admin_nf_users:
            admin_notify.read = True
            admin_notify.notification_followers.add(request.user)
            admin_notify.save()
        return JsonResponse({'ok': 'ok'})
    else:
        return HttpResponseBadRequest()


@login_required
@require_POST
def notify_read(request):
    if request.is_ajax():
        notification_id = request.POST.get("id")
        nf = Activity.objects.get(id=notification_id)
        nf.read = True
        nf.save()
        return JsonResponse({'ok': 'ok'})
    return HttpResponseBadRequest()


@login_required
@require_POST
def admin_notify_read(request):
    if request.is_ajax():
        notification_id = request.POST.get("id")
        admin_notify = AdminNotifications.objects.get(id=notification_id)
        admin_notify.notification_followers.add(request.user)
        admin_notify.save()
        return JsonResponse({'ok': 'ok'})
    return HttpResponseBadRequest()


@login_required
@require_POST
def notifications_reload(request):
    csrf_token = get_token(request)
    nfs_after_ajax = Activity.objects.filter(receiver_id=request.user).order_by('-created_at')[:5]
    return render(request, 'base/header/notifications.html', context={'nfs_after_ajax': nfs_after_ajax,
                                                                      'csrf_token': csrf_token})
