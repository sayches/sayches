from django.urls import path

from . import views

app_name = "subsections"

urlpatterns = [
    path("feed", views.home, name="home"),
    path("docs/", views.docs, name="docs"),
    path("docs/<str:slug>", views.single_docs, name="single_docs"),
    path("newsroom", views.newsroom, name="news"),
    path("newsroom/<str:slug>", views.article, name="article"),
    path("help", views.help, name="help"),
    path("remove_alert", views.remove_alert, name="remove_alert"),
    path('ads/', views.ads_step_one, name="ads"),
    path('ads/design/<str:ads_slug>/', views.ads_step_two, name="ads-step-two"),
    path('ads/plan/<str:ads_slug>/', views.ads_step_three, name="ads-step-three"),
    path('ads/checkout/<str:ads_slug>/', views.ads_step_four, name="ads-step-four"),
]
