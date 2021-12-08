from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("report", views.report_post, name="report_post"),
    path("p/<str:id>", views.post_detail, name="post_detail"),
    path("comments/<str:id>/", views.comments_detail_for_detail_post, name="comments_detail_for_detail_post"),
    path("create_post", views.create_post, name="create_post"),
    path("create_comment/<str:id>/", views.create_comment, name="create_comment"),
    path("like_post", views.post_like, name="post_like"),
    path("posts_data", views.posts_data, name='posts_data'),
    path('new_posts_data', views.new_posts_data, name='new_posts_data'),
    path("comments_data", views.comments_data_for_home_posts, name="comments_data"),
    path("post_read", views.post_read, name="post_read"),
    path("explore/", views.search, name="search"),
    path("h/<str:hashtag>", views.searchhashtag, name="search_hash"),
    path('delete', views.delete_post, name='delete-post'),
    path('delete/comment', views.delete_comment, name='delete-comment'),
    path('pin/post', views.pin_post, name='pin_post'),
    path('f/<str:flair>', views.flair_posts, name="flair_posts"),
    path('delete/post/<str:id>', views.delete_posts, name='delete-posts'),
]
