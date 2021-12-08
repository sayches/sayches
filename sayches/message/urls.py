from django.urls import path

from . import views

app_name = "message"

urlpatterns = [
    path("", views.chat_inbox, name="inbox"),
    path("inbox/delete/<int:id>/", views.delete_chat, name="delete_chat"),
    path("create_message/", views.create_messages, name="create_message"),
    path("chat_data/", views.chat_data, name="chat_data"),
    path("chat_header_data/", views.chat_header_data, name="chat_header_data"),
    path("chat_content_data/", views.old_messages_content_data, name="old_messages_content_data"),
    path("ad_chat_content_data/", views.admin_messages_content_data, name="admin_messages_content_data"),
    path("new_messages_content_data/", views.new_messages_content_data, name="new_messages_content_data"),
    path("search-users-and-chats/", views.search_for_users_and_chats, name="search-users-and-chats"),
    path("chat/<str:username>/", views.start_chat_with_user, name="chat-specfic-user"),
    path("user/json/<str:username>/", views.get_json_user, name="get-json-user"),

]
