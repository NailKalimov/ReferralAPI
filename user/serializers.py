from .models import User
from rest_framework import serializers
from adrf.serializers import ModelSerializer as aModelSerializer
from referrals.models import Referral


class aRefCodeSerializer(aModelSerializer):
    class Meta:
        model = Referral
        fields = ['code']


class aUserViewSerializer(aModelSerializer):
    referral_code = aRefCodeSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups', 'referrer', 'referral_code']


class RefCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = ['code']


class UserViewSerializer(serializers.ModelSerializer):
    referral_code = RefCodeSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups', 'referrer', 'referral_code']


class aUserCreateSerializer(aModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'referrer']

    # def acreate(self, validated_data):
    #     user = User.objects.create_user(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #         password=validated_data['password'],
    #         referrer=validated_data['referrer']
    #     )
    #     return user