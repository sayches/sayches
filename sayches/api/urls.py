from django.conf import settings
from django.urls import path, include
from rest_framework import routers

from .views import *

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

############# # Post APIs # #############
router.register('post', PublicPostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
