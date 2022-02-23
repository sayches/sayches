from django.templatetags.static import static
from django.utils import timezone
from django.utils.html import escape

from .crypto import MessagingRSA
from .models import Chat, Message


def get_companion(user, chat):
    for u in chat.members.all():
        if u != user:
            return u
    return None


def get_companion_if_unread(user, chat):
    for u in chat.members.all():
        if u != user and not chat.is_read:
            return u
    return None


user_images = 'assets/images/saychesLogo/sayches_3545x3545.png'


def get_name_for_conversation(user):
    if user.is_staff:
        return "Sayches Admin"
    if user.name:
        return user.name
    return user.username


def add_message_to_chat(chat, author, message, mate_user, request):
    message = MessagingRSA.encrypt(request, mate_user, message)
    msg = Message.objects.create(
        chat=chat, author=author, message=message['receiver_msg'], sender_message=message['sender_msg']
    )
    msg.created_at = timezone.localtime(msg.created_at)
    msg.save()



def create_chat(user, mate_user):
    chat = Chat()
    chat.save()
    chat.members.add(user, mate_user)
    return chat


def get_chat_between_two_users(user, mate_user):
    user_chats = user.chat_set.all()
    mate_user_chats = mate_user.chat_set.all()
    chat_in_between = user_chats & mate_user_chats
    return chat_in_between


def time_convert_in_local_time(msg):
    time = timezone.localtime(msg.created_at).strftime("%I:%M%p")
    return time


def get_chat_dictionary_for_context(mate_user, chat=None, request=None):
    chat_object = {
        "mate_user_id": mate_user.id,
        "chat_id": '',
        "user_img": mate_user.profile.photo_url,
        "name": mate_user.get_name_or_username(),
        "username": mate_user.username,
        "last_msg": '',
        "time_ago": '',
        "admin": 0,
        "num_of_unread_msgs": ''
    }
    if chat:
        chat_object['chat_id'] = chat.id
        messages = chat.chat_messages.order_by('created_at')
        chat_object['name'] = escape(mate_user.get_name_or_username())
        if messages:
            last_message = messages.last()
            try:
                chat_object['last_msg'] = escape(MessagingRSA.decrypt(request, last_message.sender_message))
            except:
                chat_object['last_msg'] = escape(MessagingRSA.decrypt(request, last_message.message))
            chat_object['time_ago'] = time_convert_in_local_time(last_message)
            chat_object['num_of_unread_msgs'] = messages.filter(
                author=mate_user, is_read=False).count()
    return chat_object


def get_admin_chat_dictionary_for_context(messages):
    last_message = messages.last()
    chat_object = {
        "mate_user_id": '',
        "chat_id": '',
        "user_img": static(user_images),
        "name": "Sayches",
        "last_msg": last_message.message,
        "time_ago": time_convert_in_local_time(last_message),
        "admin": 1,
        "num_of_unread_msgs": messages.filter(is_read=False).count()
    }
    return chat_object


def get_chat_meta(mate_user=None):
    if mate_user:
        chat_meta = {
            "id": '',
            "user_img": mate_user.profile.photo_url,
            "name": escape(mate_user.get_name_or_username()),
            "mate_user_id": mate_user.id,
            "username": mate_user.username,
            "admin": 0,
        }
    else:
        chat_meta = {
            "id": "",
            "user_img": static(user_images),
            "name": "Sayches",
            "mate_user_id": '',
            "admin": 1,
        }
    return chat_meta


def get_message_dictionary(msg, msg_type, request, is_admin=False):
    msg_dict = {
        "msg_type": msg_type,
        "msg_p": msg.message,
        "msg_time": time_convert_in_local_time(msg),
    }
    if is_admin:
        return msg_dict
    if msg_type == "send":
        message = MessagingRSA.decrypt(request, msg.sender_message)
    else:
        message = MessagingRSA.decrypt(request, msg.message)
    msg_dict['msg_p'] = escape(message)
    return msg_dict
