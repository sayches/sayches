from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.user_login, name='login'),
    path('steps_form/', views.steps_form, name='steps_form'),
    path('logout/', views.logout_view, name='logout'),
]
