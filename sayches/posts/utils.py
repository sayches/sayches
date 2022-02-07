import html
import json
import math
import re
from datetime import datetime as dt
from datetime import timedelta
from html.parser import HTMLParser
from urllib.parse import (parse_qsl, quote, unquote, urlencode, urlsplit, urlunsplit, )
from urllib.parse import urlparse

from django.db.models import Count
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import punycode
from django.utils.functional import Promise, keep_lazy, keep_lazy_text
from django.utils.html import escape
from django.utils.http import RFC3986_GENDELIMS, RFC3986_SUBDELIMS
from django.utils.safestring import SafeData, SafeString, mark_safe
from django.utils.text import normalize_newlines
from django.utils.timezone import localtime, now
from posts.templatetags.short_number import short_number
from users.utils import create_action

from sayches.utils.resize_image import check_image_exists
from .models import Likes, Hashtag, Mentions, LinkValidation, \
    ReportPost, Statistics, BlacklistWords

search_hash_variable = 'posts:search_hash'
profile_name_variable = 'users:profile_name'


def statistics_post(post="", report="", hashtag="", mention="", message='', anonymous_post=""):
    creation_date = localtime(now()).date()
    check_statistic = Statistics.objects.filter(date=creation_date).first()
    try:
        if check_statistic:
            if post:
                check_statistic.total_posts = post
            if report:
                check_statistic.total_reports = report
            if hashtag:
                check_statistic.total_hashtags = hashtag
            if mention:
                check_statistic.total_mentions = mention
            if message:
                check_statistic.total_messages = message
            if anonymous_post:
                check_statistic.total_anonymous = anonymous_post
            check_statistic.save()

        else:
            if post:
                create_statistic = Statistics(total_posts=post)
            if report:
                create_statistic = Statistics(total_reports=report)
            if hashtag:
                create_statistic = Statistics(total_hashtags=hashtag)
            if mention:
                create_statistic = Statistics(total_mentions=mention)
            if message:
                create_statistic = Statistics(total_messages=message)
            if anonymous_post:
                create_statistic = Statistics(total_anonymous=anonymous_post)
            create_statistic.save()
    except:
        pass

    return True


# Configuration for urlize() function.
TRAILING_PUNCTUATION_CHARS = '.,:;!'
WRAPPING_PUNCTUATION = [('(', ')'), ('[', ']')]

# List of possible strings used for bullets in bulleted lists.
DOTS = ['&middot;', '*', '\u2022', '&#149;', '&bull;', '&#8226;']

unencoded_ampersands_re = re.compile(r'&(?!(\w+|#\d+);)')
word_split_re = re.compile(r'''([\s<>"']+)''')
simple_url_re = re.compile(r'^https://[a-zA-z0_9$#./?=:;+&@{}|,%<>~]*', re.IGNORECASE)
simple_url_2_re = re.compile(r'^www.[a-zA-z$#./?=:;+&@{}|,%<>~0-9]*', re.IGNORECASE)
simple_url_3_re = re.compile(r'^http://[a-zA-z$#./?=:;+&@{}|,%<>~0-9]*', re.IGNORECASE)


@keep_lazy(str, SafeString)
def escape(text):
    """
    Return the given text with ampersands, quotes and angle brackets encoded
    for use in HTML.
    Always escape input, even if it's already escaped and marked as such.
    This may result in double-escaping. If this is a concern, use
    conditional_escape() instead.
    """
    return mark_safe(html.escape(str(text)))


_js_escapes = {
    ord('\\'): '\\u005C',
    ord('\''): '\\u0027',
    ord('"'): '\\u0022',
    ord('>'): '\\u003E',
    ord('<'): '\\u003C',
    ord('&'): '\\u0026',
    ord('='): '\\u003D',
    ord('-'): '\\u002D',
    ord(';'): '\\u003B',
    ord('`'): '\\u0060',
    ord('\u2028'): '\\u2028',
    ord('\u2029'): '\\u2029'
}

# Escape every ASCII character with a value less than 32.
_js_escapes.update((ord('%c' % z), '\\u%04X' % z) for z in range(32))


@keep_lazy(str, SafeString)
def escapejs(value):
    """Hex encode characters for use in JavaScript strings."""
    return mark_safe(str(value).translate(_js_escapes))


_json_script_escapes = {
    ord('>'): '\\u003E',
    ord('<'): '\\u003C',
    ord('&'): '\\u0026',
}


def json_script(value, element_id):
    """
    Escape all the HTML/XML special characters with their unicode escapes, so
    value is safe to be output anywhere except for inside a tag attribute. Wrap
    the escaped JSON in a script tag.
    """
    from django.core.serializers.json import DjangoJSONEncoder

    json_str = json.dumps(value, cls=DjangoJSONEncoder).translate(_json_script_escapes)
    return format_html(
        '<script id="{}" type="application/json">{}</script>',
        element_id, mark_safe(json_str)
    )


def conditional_escape(text):
    """
    Similar to escape(), except that it doesn't operate on pre-escaped strings.
    This function relies on the __html__ convention used both by Django's
    SafeData class and by third-party libraries like markupsafe.
    """
    if isinstance(text, Promise):
        text = str(text)
    if hasattr(text, '__html__'):
        return text.__html__()
    else:
        return escape(text)


def format_html(format_string, *args, **kwargs):
    """
    Similar to str.format, but pass all arguments through conditional_escape(),
    and call mark_safe() on the result. This function should be used instead
    of str.format or % interpolation to build up small HTML fragments.
    """
    args_safe = map(conditional_escape, args)
    kwargs_safe = {k: conditional_escape(v) for (k, v) in kwargs.items()}
    return mark_safe(format_string.format(*args_safe, **kwargs_safe))


def format_html_join(sep, format_string, args_generator):
    """
    A wrapper of format_html, for the common case of a group of arguments that
    need to be formatted using the same format string, and then joined using
    'sep'. 'sep' is also passed through conditional_escape.
    'args_generator' should be an iterator that returns the sequence of 'args'
    that will be passed to format_html.
    Example:
      format_html_join('\n', "<li>{} {}</li>", ((u.first_name, u.last_name)
                                                  for u in users))
    """
    return mark_safe(conditional_escape(sep).join(
        format_html(format_string, *args)
        for args in args_generator
    ))


@keep_lazy_text
def linebreaks(value, autoescape=False):
    """Convert newlines into <p> and <br>s."""
    value = normalize_newlines(value)
    paras = re.split('\n{2,}', str(value))
    if autoescape:
        paras = ['<p>%s</p>' % escape(p).replace('\n', '<br>') for p in paras]
    else:
        paras = ['<p>%s</p>' % p.replace('\n', '<br>') for p in paras]
    return '\n\n'.join(paras)


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def handle_entityref(self, name):
        self.fed.append('&%s;' % name)

    def handle_charref(self, name):
        self.fed.append('&#%s;' % name)

    def get_data(self):
        return ''.join(self.fed)


def _strip_once(value):
    """
    Internal tag stripping utility used by strip_tags.
    """
    s = MLStripper()
    s.feed(value)
    s.close()
    return s.get_data()


@keep_lazy_text
def strip_tags(value):
    """Return the given HTML with all tags stripped."""
    # Note: in typical case this loop executes _strip_once once. Loop condition
    # is redundant, but helps to reduce number of executions of _strip_once.
    value = str(value)
    while '<' in value and '>' in value:
        new_value = _strip_once(value)
        if value.count('<') == new_value.count('<'):
            # _strip_once wasn't able to detect more tags.
            break
        value = new_value
    return value


@keep_lazy_text
def strip_spaces_between_tags(value):
    """Return the given HTML with spaces between tags removed."""
    return re.sub(r'>\s+<', '><', str(value))


def smart_urlquote(url):
    """Quote a URL if it isn't already quoted."""

    def unquote_quote(segment):
        segment = unquote(segment)
        # Tilde is part of RFC3986 Unreserved Characters
        # https://tools.ietf.org/html/rfc3986#section-2.3
        # See also https://bugs.python.org/issue16285
        return quote(segment, safe=RFC3986_SUBDELIMS + RFC3986_GENDELIMS + '~')

    # Handle IDN before quoting.
    try:
        scheme, netloc, path, query, fragment = urlsplit(url)
    except ValueError:
        # invalid IPv6 URL (normally square brackets in hostname part).
        return unquote_quote(url)

    try:
        netloc = punycode(netloc)  # IDN -> ACE
    except UnicodeError:  # invalid domain part
        return unquote_quote(url)

    if query:
        # Separately unquoting key/value, so as to not mix querystring separators
        # included in query values. See #22267.
        query_parts = [(unquote(q[0]), unquote(q[1]))
                       for q in parse_qsl(query, keep_blank_values=True)]
        # urlencode will take care of quoting
        query = urlencode(query_parts)

    path = unquote_quote(path)
    fragment = unquote_quote(fragment)

    return urlunsplit((scheme, netloc, path, query, fragment))


@keep_lazy_text
def urlize(text, trim_url_limit=None, nofollow=False, autoescape=False):
    """
    Convert any URLs in text into clickable links.
    Works on http://, https://, www. links, and also on links ending in one of
    the original seven gTLDs (.com, .edu, .gov, .int, .mil, .net, and .org).
    Links can have trailing punctuation (periods, commas, close-parens) and
    leading punctuation (opening parens) and it'll still do the right thing.
    If trim_url_limit is not None, truncate the URLs in the link text longer
    than this limit to trim_url_limit - 1 characters and append an ellipsis.
    If nofollow is True, give the links a rel="nofollow" attribute.
    If autoescape is True, autoescape the link text and URLs.
    """
    safe_input = isinstance(text, SafeData)

    def trim_url(x, limit=trim_url_limit):
        if limit is None or len(x) <= limit:
            return x
        return '%s…' % x[:max(0, limit - 1)]

    def trim_punctuation(lead, middle, trail):
        """
        Trim trailing and wrapping punctuation from `middle`. Return the items
        of the new state.
        """
        # Continue trimming until middle remains unchanged.
        trimmed_something = True
        while trimmed_something:
            trimmed_something = False
            # Trim wrapping punctuation.
            for opening, closing in WRAPPING_PUNCTUATION:
                if middle.startswith(opening):
                    middle = middle[len(opening):]
                    lead += opening
                    trimmed_something = True
                # Keep parentheses at the end only if they're balanced.
                if (middle.endswith(closing) and
                        middle.count(closing) == middle.count(opening) + 1):
                    middle = middle[:-len(closing)]
                    trail = closing + trail
                    trimmed_something = True
            # Trim trailing punctuation (after trimming wrapping punctuation,
            # as encoded entities contain ';'). Unescape entities to avoid
            # breaking them by removing ';'.
            middle_unescaped = html.unescape(middle)
            stripped = middle_unescaped.rstrip(TRAILING_PUNCTUATION_CHARS)
            if middle_unescaped != stripped:
                trail = middle[len(stripped):] + trail
                middle = middle[:len(stripped) - len(middle_unescaped)]
                trimmed_something = True
        return lead, middle, trail

    def is_email_simple(value):
        """Return True if value looks like an email address."""
        # An @ must be in the middle of the value.
        if '@' not in value or value.startswith('@') or value.endswith('@'):
            return False
        try:
            p1, p2 = value.split('@')
        except ValueError:
            # value contains more than one @.
            return False
        # Dot must be in p2 (e.g. example.com)
        if '.' not in p2 or p2.startswith('.'):
            return False
        return True

    words = word_split_re.split(str(text))
    for i, word in enumerate(words):
        if '.' in word or '@' in word or ':' in word:
            # lead: Current punctuation trimmed from the beginning of the word.
            # middle: Current state of the word.
            # trail: Current punctuation trimmed from the end of the word.
            lead, middle, trail = '', word, ''
            # Deal with punctuation.
            lead, middle, trail = trim_punctuation(lead, middle, trail)

            # Make URL we want to point to.
            url = None
            klass = None
            nofollow_attr = ' rel="nofollow"' if nofollow else ''
            if simple_url_re.match(middle) or simple_url_3_re.match(middle):
                url = smart_urlquote(html.unescape(middle))
                klass = "custom-link post-short-link"

            elif simple_url_2_re.match(middle):
                url = smart_urlquote('http://%s' % html.unescape(middle))
                klass = "custom-link"
            elif ':' not in middle and is_email_simple(middle):
                local, domain = middle.rsplit('@', 1)
                try:
                    domain = punycode(domain)
                except UnicodeError:
                    continue
                url = 'mailto:%s@%s' % (local, domain)
                nofollow_attr = ''

            # Make link.
            if url:
                msg, msg2 = return_website_message(url)
                trimmed = trim_url(middle)
                if autoescape and not safe_input:
                    lead, trail = escape(lead), escape(trail)
                    trimmed = escape(trimmed)
                middle = f'<a target="_blank" confirm-msg2="{msg2}" confirm-msg="{msg}" class="{klass}" href="{escape(url + "?src=sayches.com")}"{nofollow_attr}>{trimmed}</a>'
                words[i] = mark_safe('%s%s%s' % (lead, middle, trail))
            else:
                if safe_input:
                    words[i] = mark_safe(word)
                elif autoescape:
                    words[i] = escape(word)
        elif safe_input:
            words[i] = mark_safe(word)
        elif autoescape:
            words[i] = escape(word)
        else:
            words[i] = escape(word)
    return ''.join(words)


def return_website_message(url):
    website_name = extract_webname_from_url(url)
    try:
        link_object = LinkValidation.objects.filter(url__icontains=website_name).first()
        msg = link_object.default_message
        msg2 = link_object.customized_message
    except AttributeError:
        msg = ""
        msg2 = ""
    return msg, msg2


def extract_webname_from_url(url):
    url_split_regex = re.split("://www.|.com|://", url)
    return url_split_regex[1]


def avoid_wrapping(value):
    """
    Avoid text wrapping in the middle of a phrase by adding non-breaking
    spaces where there previously were normal spaces.
    """
    return value.replace(" ", "\xa0")


def html_safe(klass):
    """
    A decorator that defines the __html__ method. This helps non-Django
    templates to detect classes whose __str__ methods return SafeString.
    """
    if '__html__' in klass.__dict__:
        raise ValueError(
            "can't apply @html_safe to %s because it defines "
            "__html__()." % klass.__name__
        )
    if '__str__' not in klass.__dict__:
        raise ValueError(
            "can't apply @html_safe to %s because it doesn't "
            "define __str__()." % klass.__name__
        )
    klass_str = klass.__str__
    klass.__str__ = lambda self: mark_safe(klass_str(self))
    klass.__html__ = lambda self: str(self)
    return klass


def like_action(user, post):
    action = ''
    reaction_status = Likes.objects.filter(user=user, post=post)
    if reaction_status:
        reaction_status = Likes.objects.filter(user=user, post=post)
        for r in reaction_status:
            action = r.reaction_name
    else:
        action = 'unlike'

    return action


def post_is_read(user, post):
    flag = ''
    followers = post.post_followers.all()
    if user in followers:
        flag = 'read'
    else:
        flag = 'unread'

    return flag


def get_hashtags(post):
    post_text = post.text
    if post.post_option == "normal":
        words_list = post_text.split()
        hashtags_list = [word for word in words_list if word[0] == '#']
    else:
        hashtags_list = [word for word in post_text if word[0] == '#']
    if hashtags_list:
        for i in hashtags_list:
            hashtag = Hashtag.objects.filter(implicit_name=i).first()
            if hashtag:
                hashtag.hashtag_counter += 1
                hashtag.save()
            else:
                hashtag = Hashtag.objects.create(explicit_name=i)
                hashtag.author = post.user
                hashtag.save()
            post.hashtags.add(hashtag)
    total_hashtag_count = Hashtag.objects.all().count()
    statistics_post(hashtag=total_hashtag_count)
    return None


def get_mentions(post):
    post_text = post.text
    if post.post_option == "normal":
        words_list = post_text.split()
        mentions_list = [word for word in words_list if word[0] == '@']
    else:
        mentions_list = [word for word in post_text if word[0] == '@']

    if mentions_list:
        for i in mentions_list:
            mention = Mentions.objects.filter(implicit_name=i).first()
            if not mention:
                mention = Mentions.objects.create(explicit_name=i)
            post.mentions.add(mention)
    total_maintain_count = Mentions.objects.all().count()
    statistics_post(mention=total_maintain_count)

    return None


def get_comment_hashtags(comment):
    comment_text = comment.text
    words = comment_text.split()
    hashtags_list = [word for word in words if word[0] == '#']
    if hashtags_list:
        for i in hashtags_list:
            hashtag = Hashtag.objects.filter(implicit_name=i).first()
            if hashtag:
                hashtag.save()
            else:
                hashtag = Hashtag.objects.create(explicit_name=i, author=comment.user)

            hashtag.hashtag_counter += 1
            comment.chashtags.add(hashtag)
    return None


def prevent_comment_hashtag_repetition(comment):
    comment_text = comment
    words_list = comment.split()
    hashtags_list = [word for word in words_list if word[0] == '#']
    mentions_list = [word for word in words_list if word[0] == '@']

    for hashtag in hashtags_list:
        hashtag = Hashtag.objects.filter(implicit_name=hashtag).first()
        hashtag_decode = "/h/" + str(hashtag).replace('#', '%23', 1)
        comment_text = convert_to_anchor_tag(comment_text, hashtag_decode, hashtag)

    for mention in mentions_list:
        mention = Mentions.objects.filter(implicit_name=mention).first()
        user_url = "/u/" + str(mention).replace('@', '%40', 1)
        comment_text = convert_to_anchor_tag(comment_text, user_url, mention)

    return comment_text


def prevent_hashtag_repetition(post):
    post_text = post.text
    if post.post_option == "normal":
        words_list = post_text.split()
        hashtags_list = [word for word in words_list if word[0] == '#']
        mentions_list = [word for word in words_list if word[0] == '@']

        for hashtag in hashtags_list:
            hashtag = Hashtag.objects.filter(implicit_name=hashtag).first()

            hashtag_decode = "/h/" + str(hashtag).replace('#', '%23', 1)
            post_text = convert_to_anchor_tag(post_text, hashtag_decode, hashtag)

        for mention in mentions_list:
            mention = Mentions.objects.filter(implicit_name=mention).first()
            user_url = "/u/" + str(mention).replace('@', '%40', 1)
            post_text = convert_to_anchor_tag(post_text, user_url, mention)
    return post_text


def convert_to_anchor_tag(post_text, url, anchor_text):
    href_url = f'<a href={escape(str(url))}>{(str(anchor_text))}</a>'
    post_text = post_text.replace(str(anchor_text), href_url)
    return mark_safe(post_text)


def format_post_type_data(user, post, json_object):
    if post.post_option == "normal":
        hashtags = list(Hashtag.objects.filter(posts__in=[post]).values_list("explicit_name", flat=True))
        mentions = list(Mentions.objects.filter(posts__in=[post]).values_list("explicit_name", flat=True))

        json_object['hashtags'] = [{
            "hashtag_name": hashtag,
            "hashtag_link": reverse(search_hash_variable, args=[str(hashtag)]),
        } for hashtag in hashtags]

        json_object['mentions'] = [{
            "mention_name": mention,
            "mention_link": reverse(profile_name_variable, args=[str(mention)]),
        } for mention in mentions]

    return json_object


def get_profile_pic(post):
    return post.user.profile.photo_url


def posts_to_json(request, user, posts):
    total_posts = len(posts)
    objects_list = []
    action = ''
    flag = ''

    for post in posts:
        image_url = get_profile_pic(post)
        post_followers = post.post_followers.all().count()

        if user.is_authenticated:
            action = like_action(user, post)
            flag = post_is_read(request.user, post)
        else:
            action = 'unlike'
            flag = 'unread'

        if action == 'unlike':
            do_status = 'do'
        else:
            do_status = 'undo'

        post_reactions = Likes.objects.filter(post=post)
        reaction_number = short_number(post_reactions.count())
        delete_time = (post.created_at + timedelta(hours=post.user.profile_update_time))
        re = delete_time - dt.now(timezone.utc)
        total_hours = (re.days * 24) + math.floor(re.seconds / 3600)

        if request.user.is_authenticated:
            current_user = request.user
            user_reaction = post_reactions.filter(user=request.user).last()
            user_reaction = user_reaction.reaction_name if user_reaction else None
        else:
            current_user = None
            user_reaction = 'guest'
        post_reactions_dict = get_post_reaction_count(post_reactions)
        post_reactions_dict["user_reaction"] = user_reaction
        post_reactions_dict["login_user"] = request.user.user_hash if current_user else None
        json_object = {}
        check = False
        if post.media:
            check = check_image_exists(post.media)
        json_object = {
            "id": post.id,
            "user_img": image_url,
            "name": escape(post.user.display_user_name()),
            "user_name": escape(post.user.user_hash),
            "user_nickname": escape(post.user.get_alias_display()),
            "date": post.created_at.strftime("%d/%m/%Y %I:%M %p"),
            "created_at": post.created_at.isoformat(),
            "remaining_time": total_hours,
            "post_count": post_followers,
            "post_p": urlize(prevent_hashtag_repetition(post)),
            "user_page": reverse(profile_name_variable, args=[post.user.user_hash]),
            "pinned": post.pinned_post if type(posts) is not list else 'false',
            "post_flair": post.flair,
            "post_option": post.post_option,
            "post_media": post.media.url if check else 'null',
            "flag": flag,
            "do_status": do_status,
            "bio": escape(post.user.profile.bio),
            "reaction_number": reaction_number,
            "reaction_status": "action",
            "total_posts": total_posts
        }

        format_post_type_data(user, post, json_object)
        json_object.update(post_reactions_dict)
        objects_list.append(json_object)
    return objects_list


def single_post_to_json(user, post):
    if post.user.name == "":
        name = post.user.user_hash
    else:
        name = post.user.name

    image_url = get_profile_pic(post)

    post_followers = post.post_followers.all().count()

    post_reactions = Likes.objects.filter(post=post)
    post_reactions_dict = get_post_reaction_count(post_reactions)

    flag = 'read'
    if user and user.is_authenticated:
        flag = post_is_read(user, post)

        user_reaction = post_reactions.filter(user=user).last()
        post_reactions_dict["user_reaction"] = user_reaction.reaction_name if user_reaction else None
    else:
        user = None
        post_reactions_dict["user_reaction"] = 'guest'

    do_status = 'do'
    if flag == 'unlike':
        do_status = 'undo'

    post_url = "/p/" + post.id
    post_p = urlize(prevent_hashtag_repetition(post))
    reaction_number = Likes.objects.filter(post=post).count()
    delete_time = (post.created_at + timedelta(hours=post.user.profile_update_time))
    re = delete_time - dt.now(timezone.utc)
    total_hours = (re.days * 24) + math.floor(re.seconds / 3600)
    check = False
    if post.media:
        check = check_image_exists(post.media)
    json_object = {}
    json_object['id'] = post.id
    json_object['user_img'] = image_url
    json_object["name"] = escape(post.user.display_user_name())
    json_object["date"] = post.created_at.strftime("%d/%m/%Y %I:%M %p")
    json_object["remaining_time"] = total_hours
    json_object["post_count"] = post_followers
    json_object["post_p"] = post_p
    json_object["reaction_number"] = reaction_number
    json_object["reaction_status"] = "action"
    json_object["is_pin_post"] = post.pinned_post
    json_object["post_media"] = post.media.url if check else 'null',
    json_object["post_url"] = post_url
    json_object["user_nickname"] = escape(post.user.get_alias_display())
    json_object["user_name"] = escape(post.user.user_hash)
    json_object["user_page"] = reverse(profile_name_variable, args=[post.user.user_hash])
    json_object["flag"] = flag
    json_object["do_status"] = do_status
    json_object["bio"] = escape(post.user.profile.bio)
    json_object["pinned"] = post.pinned_post
    json_object["post_flair"] = post.flair
    json_object["post_option"] = post.post_option

    json_object['post_repoted'] = False
    if user:
        json_object["login_user"] = user.user_hash
        json_object["is_his_post"] = (user == post.user)
        check_post_report = ReportPost.objects.filter(post_reporter=user, post_user=post.user,
                                                      post_id=post.id).first()
        if check_post_report:
            json_object['post_repoted'] = True

    format_post_type_data(user, post, json_object)
    json_object.update(post_reactions_dict)

    return json_object

def send_notifications_to_user_bell_list(user, post):
    user_bell_list = user.ring_from.all()
    for ring in user_bell_list:
        create_action(user, ring.user, "posted a new post", post.text, activity_type="bell", target=post)


def get_post_reaction_count(post_reactions):
    reaction_list = post_reactions.filter(reaction_name__in=["🥚"]).values(
        'reaction_name').annotate(total=Count('id')).order_by('reaction_name')
    reaction_count = {
        "egg_number": 0,
    }
    for reaction_dic in reaction_list:
        if reaction_dic.get("reaction_name") == "🥚":
            reaction_count.update({"egg_number": reaction_dic.get("total")})

    return reaction_count


def get_parsed_meta_url(request, redirect="/"):
    url = request.META.get('HTTP_REFERER')
    parsed_uri = urlparse(url)
    return url


def replace_profanity_words(str):
    profanity_word = BlacklistWords.get_words(is_emoji=False)
    replaced_text = ''
    regex = re.compile(rf"\b({'|'.join(profanity_word)})\b", flags=re.IGNORECASE)
    clean_text = re.sub(regex, replaced_text, str)
    profanity_emoji = BlacklistWords.get_words(is_emoji=True)
    for emoji in profanity_emoji:
        clean_text = clean_text.encode('unicode-escape').decode('utf-8').replace(emoji, replaced_text)
        clean_text = clean_text.encode('utf-8').decode('unicode-escape')
    return clean_text
