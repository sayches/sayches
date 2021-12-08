from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from users.models import BlacklistUser

from .models import Chat, SaychesMessage
from .utils import (
    get_companion, create_chat, add_message_to_chat, get_chat_between_two_users,
    get_chat_dictionary_for_context, get_admin_chat_dictionary_for_context,
    get_chat_meta, get_message_dictionary)

User = get_user_model()


def redirect_if_messages_disabled(func):
    def wrapper(request, *args, **kwargs):
        try:
            disable_messages = request.user.profile.disable_messages
            if disable_messages:
                return redirect('subsections:home')
            else:
                return func(request, *args, **kwargs)
        except Exception as e:
            return redirect('subsections:home')

    return wrapper


@redirect_if_messages_disabled
@require_GET
def delete_chat(request, id):
    chat = get_object_or_404(Chat, id=id)
    chat.delete()
    return redirect('message:inbox')


@login_required
@redirect_if_messages_disabled
@require_GET
def chat_inbox(request):
    check_message_block = BlacklistUser.objects.filter(user=request.user, on_message=True).first()
    is_message_block = False
    if check_message_block:
        is_message_block = True
    context = {"is_message_block": is_message_block}
    return render(request, 'messages/inbox.html', context)


@redirect_if_messages_disabled
@require_POST
def create_messages(request):
    if request.is_ajax():
        msg_content = request.POST.get("msg_content")
        mate_user_id = request.POST.get("mate_user_id")
        if mate_user_id:
            mate_user = get_object_or_404(User, id=mate_user_id)
            chat_in_between = get_chat_between_two_users(
                request.user, mate_user).first()
            if chat_in_between:
                add_message_to_chat(chat_in_between, request.user, msg_content, mate_user, request)
                chat_in_between.is_read = False
                chat_in_between.save()
                return JsonResponse({'ok': 'ok'})
            else:
                chat = create_chat(request.user, mate_user)
                add_message_to_chat(chat, request.user, msg_content)
                return JsonResponse({'ok': 'ok'})
        return JsonResponse({'ok': 'no'})
    return HttpResponseBadRequest()


@require_GET
def chat_data(request):
    if request.is_ajax():
        user = request.user
        chat_context_list = []
        messages = SaychesMessage.objects.filter(user=user).order_by('created_at')
        if messages:
            chat_context_list.append(
                get_admin_chat_dictionary_for_context(messages))
        chats = user.chat_set.order_by('-time_of_last_msg')[:20]
        for chat in chats:
            mate_user = get_companion(user, chat)
            if mate_user is None:
                continue
            if mate_user.is_staff:
                continue
            if not mate_user.profile.disable_messages:
                chat_context_list.append(
                    get_chat_dictionary_for_context(mate_user, chat, request))
        return JsonResponse(chat_context_list, safe=False)
    return HttpResponseBadRequest()


@require_GET
def chat_header_data(request):
    if request.is_ajax():
        user = request.user
        chat_id = request.GET.get("chat_id")
        mate_user_id = request.GET.get("mate_user_id")
        if mate_user_id:
            mate_user = get_object_or_404(User, id=mate_user_id)
            chat_in_between = get_chat_between_two_users(user, mate_user).first()
            if chat_in_between:
                unread_messages = chat_in_between.chat_messages.filter(is_read=False)
                unread_messages.update(is_read=True)
                chat_in_between.is_read = True
                chat_in_between.save()
            return JsonResponse([get_chat_meta(mate_user)], safe=False)
        else:
            sayches_msgs = SaychesMessage.objects.filter(user=request.user)
            sayches_msgs.update(is_read=True)
            return JsonResponse([get_chat_meta()], safe=False)
    return HttpResponseBadRequest()


@require_GET
def admin_messages_content_data(request):
    if request.is_ajax():
        chat_content = []
        sayches_msgs = SaychesMessage.objects.filter(user=request.user)
        for msg in sayches_msgs:
            chat_content.append(get_message_dictionary(msg, "receive", request, is_admin=True))
        return JsonResponse(chat_content, safe=False)
    return HttpResponseBadRequest()


@require_GET
def old_messages_content_data(request):
    if request.is_ajax():
        chat_content = []
        user = request.user
        mate_user_id = request.GET.get("mate_user_id")
        if mate_user_id:
            mate_user = get_object_or_404(User, id=mate_user_id)
            chat_in_between = get_chat_between_two_users(user, mate_user).first()
            if chat_in_between:
                messages = chat_in_between.chat_messages.all()
                for msg in messages:
                    if msg.author == user:
                        msg_type = "send"
                    else:
                        msg_type = "receive"
                    chat_content.append(get_message_dictionary(msg, msg_type, request))
        return JsonResponse(chat_content, safe=False)
    return HttpResponseBadRequest()


@require_GET
def new_messages_content_data(request):
    if request.is_ajax():
        chat_content = []
        user = request.user
        mate_user_id = request.GET.get("mate_user_id")
        if mate_user_id:
            mate_user = get_object_or_404(User, id=mate_user_id)
            chat_in_between = get_chat_between_two_users(user, mate_user)
            chat = chat_in_between.first()
            if chat:
                messages = chat.chat_messages.filter(new=True)
                for msg in messages:
                    if msg.author == user:
                        msg_type = "send"
                    else:
                        msg_type = "receive"
                    msg.new = False
                    msg.save()
                    chat_content.append(get_message_dictionary(msg, msg_type))
        return JsonResponse(chat_content, safe=False)
    return HttpResponseBadRequest()


@require_GET
def search_for_users_and_chats(request):
    if request.is_ajax():
        chat_context_list = []
        key = request.GET.get('key', None)
        if key:
            filtered_users = User.objects.filter(
                username__icontains=key, is_staff=False)[:20]
            for user in filtered_users:
                if not user.profile.disable_messages:
                    chat_in_between = get_chat_between_two_users(
                        request.user, user).first()
                    chat_context_list.append(
                        get_chat_dictionary_for_context(user, chat_in_between))
            if key.lower() in 'sayches':
                messages = SaychesMessage.objects.filter(
                    user=request.user).order_by('created_at')
                if messages:
                    chat_context_list.append(
                        get_admin_chat_dictionary_for_context(messages))
        return JsonResponse(chat_context_list, safe=False)
    return HttpResponseBadRequest()


@redirect_if_messages_disabled
@require_GET
def start_chat_with_user(request, username):
    user = User.objects.get(username=username)
    if user.profile.disable_messages:
        return redirect('subsections:home')
    context = {"mate_username": username}
    return render(request, 'messages/inbox.html', context)


@require_GET
def get_json_user(request, username):
    if request.is_ajax():
        mate_user = get_object_or_404(User, username=username)
        chat_in_between = get_chat_between_two_users(
            request.user, mate_user).first()
        mate_user_chat = get_chat_dictionary_for_context(mate_user, chat_in_between)
        return JsonResponse(mate_user_chat)
    return HttpResponseBadRequest()
