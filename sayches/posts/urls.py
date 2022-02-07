from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("report", views.report_post, name="report_post"),
    path("p/<str:id>", views.post_detail, name="post_detail"),
    path("create_post", views.create_post, name="create_post"),
    path("like_post", views.post_like, name="post_like"),
    path("posts_data", views.posts_data, name='posts_data'),
    path('new_posts_data', views.new_posts_data, name='new_posts_data'),
    path("post_read", views.post_read, name="post_read"),
    path("explore/", views.search, name="search"),
    path("h/<str:hashtag>", views.searchhashtag, name="search_hash"),
    path('delete', views.delete_post, name='delete-post'),
    path('pin/post', views.pin_post, name='pin_post'),
    path('f/<str:flair>', views.flair_posts, name="flair_posts"),
    path('delete/post/<str:id>', views.delete_posts, name='delete-posts'),
]
