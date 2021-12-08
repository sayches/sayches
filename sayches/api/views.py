from posts.models import Post
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import *


############# # Post APIs # #############


class PublicPostViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = PublicPostSerializer
    queryset = Post.objects.all()
    http_method_names = ['get']
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Post.objects.filter(user=self.request.user)
        return queryset
