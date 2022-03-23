from datetime import datetime, timedelta

from ads.models import CreateAds
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from posts.utils import get_parsed_meta_url, replace_profanity_words
from subsections.models import Ads
from users.models import BlacklistUser, FromSayches
from users.models import User
from users.utils import create_action, get_mention_tags

from config.choices import FLAIR_CHOICES
from config.settings.base import SET_INTERVAL_ALLOW, BASE_URL
from .forms import SearchPost
from .models import Post, Likes, Hashtag, ReportPost, PostsTimestamp
from .utils import get_hashtags, get_mentions, posts_to_json, single_post_to_json, send_notifications_to_user_bell_list

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@login_required
@require_POST
def report_post(request):
    url = get_parsed_meta_url(request, "/")
    if request.POST:
        reason = request.POST.get("reason")
        postid = request.POST.get("postid")
        post_url = request.POST.get("post_url")
        post = get_object_or_404(Post, id=postid)
        report_post = ReportPost(post_reporter=request.user, post_user=post.user, post_id=post,
                                 complaint_date=datetime.now(), flagging_reason=reason)
        report_post.post_text = post.text
        report_post.post_url = post_url
        report_post.save()
        admin_email_body = 'Hey Admin, There is a report on a post.'
        FromSayches.from_sayches(title='Post Reported', message=admin_email_body,
                                    to=User.objects.filter(is_superuser=True).last())
        render_body = render_to_string('feed/post/report_post_email.html',
                                       {'username': post.user.username, 'post_id': postid, 'post_url': post_url,
                                        'post_text': post.text, 'domain': BASE_URL})
        FromSayches.from_sayches(title='Complaint regarding your post / PI: {0}'.format(postid),
                                 message=render_body, to=report_post.post_user)
    return HttpResponseRedirect(url)


@require_GET
def post_detail(request, id):
    user = request.user if request.user.is_authenticated else None
    post = get_object_or_404(Post, id=id)
    post.created_at = timezone.localtime(post.created_at)
    post.save()
    data = []
    hashtags = Hashtag.objects.all()[:3]
    is_block_post = False
    is_search_user_profile = False

    if user:
        check_black_list = BlacklistUser.objects.filter(user=user, on_post=True).first()
        if check_black_list:
            is_block_post = True
        check_over_all_block = BlacklistUser.objects.filter(Q(user=user), Q(on_post=True) | Q(on_login=True) | Q(
            on_message=True)).first()

        if check_over_all_block:
            is_search_user_profile = True

    check_post_report = None
    if request.user.is_authenticated:
        check_post_report = ReportPost.objects.filter(post_reporter=request.user, post_id=post).first()

    context = {
        'post_id': post.id,
        'check_post_report': check_post_report,
        'hashtags': hashtags,
        'post': post,
        'backbtn': True,
        "is_block_post": is_block_post,
        "is_search_user_profile": is_search_user_profile
    }
    if request.is_ajax():
        json_object = single_post_to_json(user, post)
        data.append(json_object)
        return JsonResponse(data, safe=False)
    return render(request, "feed/post/post.html", context)



def format_posts(request, user, posts):
    sort_type = request.GET.get('sortby', None)

    if sort_type == 'oldest':
        posts = sorted(posts, key=lambda p: p.created_at)
    else:
        posts = sorted(posts, key=lambda p: p.created_at, reverse=True)
    data = posts_to_json(request, user, posts)
    paginator = Paginator(data, 10)
    page_number = request.GET.get('page', 1)
    try:
        page_data = paginator.page(page_number)
        data = page_data.object_list
    except EmptyPage:
        data = []

    return data


# @cache_page(CACHE_TTL)
@require_GET
def posts_data(request):
    if request.is_ajax():
        posts = []
        user = request.user
        if request.user.is_authenticated:
            posts_obj = Post.objects.all().exclude(restrict=True)[:100]
        else:
            posts_obj = Post.objects.all().exclude(restrict=True)[:10]

        for p in posts_obj:
            posts.append(p)
        data = format_posts(request, user, posts)
        return JsonResponse(data, safe=False)
    return HttpResponseBadRequest()


@require_GET
def new_posts_data(request):
    if request.is_ajax():
        last_post_created_at = request.GET.get("datetime", "1970-01-01T12:00:00.00+0000")
        last_post_created_at = post_formated_data(request, last_post_created_at)
        posts = []
        posts = sorted(posts, key=lambda p: p.created_at, reverse=True)
        data = posts_to_json(request, request.user, posts)
        return JsonResponse(data, safe=False)
    else:
        return HttpResponseBadRequest()


def post_formated_data(request, last_post_created_at):
    last_post_created_at = last_post_created_at.replace(' ', '+')
    if ":" == last_post_created_at[-3]:
        last_post_created_at = last_post_created_at[:-3] + last_post_created_at[-2:]

    last_post_created_at = datetime.strptime(last_post_created_at, '%Y-%m-%dT%H:%M:%S.%f%z')
    ts = last_post_created_at.timestamp()
    last_post_created_at = datetime.fromtimestamp(ts, tz=timezone.utc)

    if not last_post_created_at:
        return JsonResponse({}, safe=False)
    return last_post_created_at

@login_required
@require_POST
def create_post(request):
    if request.is_ajax():
        data = []

        if request.POST:
            text = request.POST.get("text")
            flair = request.POST.get("flair")
            media = request.FILES.get('media')
            check_black_list = BlacklistUser.objects.filter(user=request.user, on_post=True).first()
            if not check_black_list:
                limit_checker = rate_limitor_for_post(request=request, user=request.user)
                if limit_checker:
                    cleaned_text = replace_profanity_words(text)
                    post = create_post_entry(user=request.user, flair=flair, post_option="normal", text=cleaned_text,
                                             media=media)
                    get_mention_tags(text=post.text, sender=request.user, target=post)
                    get_hashtags(post)
                    get_mentions(post)
                    post_object = single_post_to_json(request.user, post)
                    data.append(post_object)
                    send_notifications_to_user_bell_list(request.user, post)
        return JsonResponse(data, safe=False)
    return HttpResponseBadRequest()


def create_post_entry(user, flair, post_option, text, media=None):
    post = Post.objects.create(user=user, flair=flair, post_option=post_option, text=text, media=media)
    post.save()
    post.created_at = timezone.localtime(post.created_at)
    post.save()
    user_post_timestamp = PostsTimestamp.objects.create(user=user, post_id=post.id)
    user_post_timestamp.post_timestamp = timezone.localtime(post.created_at)
    user_post_timestamp.save()
    return post


def rate_limitor_for_post(request, user):
    current_time = timezone.localtime(timezone.now())
    time_interval = current_time - timedelta(minutes=SET_INTERVAL_ALLOW)
    check_interval = Post.objects.filter(user=user, created_at__range=(time_interval, current_time)).count()

    if check_interval >= 1:
        request.session['rate_limiter_post'] = True
        return False
    else:
        request.session['rate_limiter_post'] = False
        return True


@login_required
@require_POST
def post_like(request):
    if request.is_ajax():
        user = request.user
        post_id = request.POST.get('id')
        action = request.POST.get('action')
        if post_id and action:
            try:
                post = Post.objects.get(id=post_id)
                if action != 'unlike':
                    obj, created_at = Likes.objects.update_or_create(user=user, post=post, defaults={
                        'user': user, 'post': post, 'reaction_name': action})
                    post.post_followers.add(user)
                    if not request.user == post.user:
                        emojis = {
                            '🥚': '🥚',
                        }
                        create_action(sender=request.user, receiver=post.user,
                                      verb="egged your post {}".format(emojis[obj.reaction_name]), text=None,
                                      target=post)
                else:
                    Likes.objects.filter(user=user, post=post).delete()
                reaction_number = Likes.objects.filter(post=post).count()
                return JsonResponse({'status': 'ok', reaction_number: 'reaction_number'})
            except Exception:
                pass
        return JsonResponse({'status': 'ko', 'action': action})
    return HttpResponseBadRequest()


@login_required
@require_POST
def post_read(request):
    if request.is_ajax():
        post_id = request.POST.get("id")
        post = Post.objects.get(id=post_id)
        post.post_followers.add(request.user)
        return JsonResponse({'ok': 'ok'})
    return HttpResponseBadRequest()


@require_http_methods(["GET", "POST"])
def search(request):
    user = request.user

    form = SearchPost()
    posts = ''
    users = []
    data = ''
    hashtags = Hashtag.objects.all()[:3]
    if request.method == 'GET':
        form = SearchPost(request.GET)
        query = request.GET.get('search', None)
        if query:
            posts = Post.objects.filter(text__icontains=query)
            hashtags = Hashtag.objects.filter(explicit_name__icontains=query)[:20]
            all_users = User.objects.filter(Q(name__icontains=query) | Q(username__icontains=query)).exclude(
                is_superuser=True)[:20]

            for u in all_users:
                current_user = {
                    'user_hash': u.user_hash,
                    'id': u.id,
                    'profile_photo': u.profile.photo,
                    'photo_url': u.profile.photo_url if u.profile.photo_url else None,
                    'name': u.name,
                    'username': u.username,
                }
                users.append(dict(current_user))

        if request.is_ajax():
            data = format_posts(request, user, posts)
            return JsonResponse(data, safe=False)
    if search:
        ads = CreateAds.objects.filter(keywords__slug__icontains=query)
        if ads:
            ads = ads.first()
        else:
            ads = CreateAds.objects.order_by('?').first()
    else:
        ads = CreateAds.objects.order_by('?').first()
    try:
        Ads.ad_impressions(ads)
    except:
        pass

    context = {
        'form': form,
        'posts': posts,
        'hashtags': hashtags,
        'users': users,
        'data': data,
        'query': query,
    }
    if ads:
        context['ads'] = ads

    if request.user.is_authenticated:
        check_black_list = BlacklistUser.objects.filter(user=request.user, on_post=True).first()
        context['is_block_post'] = False
    else:
        check_black_list = None
    if check_black_list:
        context['is_block_post'] = True

    return render(request, 'feed/search/search.html', context)


@require_http_methods(["GET", "POST"])
def searchhashtag(request, hashtag):
    user = request.user
    form = SearchPost()
    posts = ''
    users = []
    data = ''
    hashtags = Hashtag.objects.all()[:3]
    hashtag_post_user, counter, status = get_hashtag_writer(hashtag)
    search_on = None
    if request.method == 'GET':
        form = SearchPost(request.GET)
        query = request.GET.get('search')
        if hashtag:
            query = hashtag
        if query:
            posts = Post.objects.filter(text__icontains=query)
            hashtags = Hashtag.objects.filter(explicit_name__icontains=query)[:20]
            check_users = [post.user for post in posts]
            users = list(set(check_users))
            search_on = query.split('#')[1]
        if request.is_ajax():
            data = format_posts(request, user, posts)
            return JsonResponse(data, safe=False)

    try: 
        check_black_list = BlacklistUser.objects.filter(user=request.user, on_post=True).first()
    except:
        check_black_list = None
    is_block_post = False
    if check_black_list:
        is_block_post = True
    ads = CreateAds.objects.order_by('?').first()
    try:
        Ads.ad_impressions(ads)
    except:
        pass

    context = {
        "query": search_on,
        'form': form,
        'posts': posts,
        'hashtags': hashtags,
        'users': users,
        'data': data,
        'hashtag': hashtag,
        'hashtag_post_user': hashtag_post_user,
        'counter': counter,
        'status': status,
        "is_block_post": is_block_post
    }
    if ads:
        context['ads'] = ads
    return render(request, 'feed/search/search.html', context)


def get_hashtag_writer(hashtag):
    hashtag = Hashtag.objects.filter(explicit_name__icontains=hashtag).first()
    if hashtag:
        hashtag_post_user = hashtag.author if hashtag.author else 'Anonymous'
        return hashtag_post_user, hashtag.hashtag_counter, hashtag.get_status_display()
    else:
        return None, None, None


@require_GET
def flair_posts(request, flair):
    posts = None
    data = None
    user = request.user
    flair_name = dict(FLAIR_CHOICES).get(flair)
    if request.method == 'GET' and flair:
        if flair:
            posts = Post.objects.filter(flair__iexact=flair)
        if request.is_ajax():
            data = format_posts(request, user, posts)
            return JsonResponse(data, safe=False)
    context = {'posts': posts, 'data': data, 'flair': flair, 'flair_name': flair_name}
    return render(request, 'feed/flair/flair.html', context)


@login_required
@require_POST
def delete_post(request):
    post_id = request.POST.get('post_id')
    post_to_be_deleted = get_object_or_404(Post, id=post_id)
    if request.user != post_to_be_deleted.user:
        return redirect('subsections:home')
    post_to_be_deleted.delete()
    return redirect('subsections:home')

@login_required
@require_POST
def pin_post(request):
    if request.is_ajax():
        post_id = request.POST.get('id')
        new_pin_post = get_object_or_404(Post, id=post_id)

        other_pin_post = Post.objects.filter(user=request.user, pinned_post=True).first()
        if new_pin_post:
            new_pin_post.pinned_post = not new_pin_post.pinned_post
            new_pin_post.save()
            if other_pin_post:
                other_pin_post.pinned_post = False
                other_pin_post.save()
        return JsonResponse({'pinned': new_pin_post.pinned_post})
    return HttpResponseBadRequest()


@login_required
@require_GET
def delete_posts(request, id):
    post_id = id
    post_for_delete = get_object_or_404(Post, id=post_id)
    if request.user != post_for_delete.user:
        return redirect('subsections:home')
    post_for_delete.delete()
    return redirect('subsections:home')
