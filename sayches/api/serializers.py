from posts.models import Post
from rest_framework import serializers
from users.models import User, Profile


############# # User APIs # #############

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['photo', 'photo_url', 'bio', 'pgp_fingerprint', 'btc_address', 'website']


class PublicUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'name', 'profile', 'warrant_canary']


############# # Post APIs # #############

class PublicPostSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer()

    class Meta:
        model = Post
        fields = ['id', 'user', 'text', 'flair', 'post_option', 'pinned_post', 'media']
