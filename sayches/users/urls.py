from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path('<int:id>/', views.profile_detail, name="profile"),
    path('settings', views.profile_update, name="profile_update"),
    path('update/account_delete_time', views.AutoAccountDeleteTime.as_view(), name="auto_account_delete_time"),
    path('update/nick', views.UpdateNickView.as_view(), name="profile_nickname"),
    path('update/toggle', views.UpdateToggleView.as_view(), name="profile_toggles"),
    path('u/<str:username>', views.profile_detail_name, name="profile_name"),
    path('forget/<str:username>', views.forget_user, name='forget-user'),
    path('set-or-remove-bell/<str:username>/', views.set_or_remove_bell_for_user, name="set-or-remove-bell"),
    path('ping-user/<str:username>', views.ping_user, name="ping-user"),
    path('pong-user/<int:id>/', views.pong_user, name="pong-user"),
    path('report_user', views.report_user, name="report_user"),
    path("notifications/notifications_counter", views.notification_number, name="notification_number"),
    path("notifications/mark_all", views.mark_all_read, name="mark_all_read"),
    path("notifications/notify_read", views.notify_read, name="notify_read"),
    path("notifications/admin_notify_read", views.admin_notify_read, name="admin_notify_read"),
    path("notifications/notifications_reload/", views.notifications_reload, name="notifications_reload"),
    path("export/<str:username>", views.export_my_data, name="export_my_data"),
    path('search/user', views.search_user, name='search-user'),
]
