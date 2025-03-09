from .models import User
from rest_framework import serializers
from referrals.models import Referral


class RefCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = ['code']


class UserViewSerializer(serializers.HyperlinkedModelSerializer):
    referral_code = RefCodeSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups', 'referrer', 'referral_code']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'referrer']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            referrer=validated_data['referrer']
        )
        return user
