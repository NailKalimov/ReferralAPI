from copy import copy
from trace import Trace

from adrf.viewsets import ModelViewSet as aModelViewSet
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample
from rest_framework import permissions
from rest_framework.response import Response
from adrf.views import APIView as aAPIView
from rest_framework import status
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK

from .models import User
from .serializers import aUserViewSerializer, aUserCreateSerializer
from .utils import send_referral_code_to_email_for_current_user


@extend_schema_view(
    retrieve=extend_schema(summary="User detail"),
    list=extend_schema(
        summary="List of users")
)
class UserViewSet(aModelViewSet):
    http_method_names = ['get']
    User = get_user_model()
    serializer_class = aUserViewSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class ReferralUserCreate(aAPIView):
    serializer_class = aUserCreateSerializer


    @extend_schema(
        summary="New user",
        examples=[
            OpenApiExample(
                "Post example",
                request_only=True,
                value={
                    "username": "testuser_xxx",
                    "email": "user@example.com",
                    "password": "string",
                }
            )
        ]
    )
    async def post(self, request, ref_code=None):
        data = copy(request.data)
        if ref_code:
            data['referrer'] = await sync_to_async(User.objects.get)(referral_code__code=ref_code)
        serializer = aUserCreateSerializer(data=data)
        if await sync_to_async(serializer.is_valid)():
            await serializer.asave()
            return Response(status=status.HTTP_201_CREATED,
                            data="User registered successfully")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# async view
class ReferralUserListView(aAPIView):
    serializer_class = aUserViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(summary="List of invited users")
    async def get(self, request, pk):
        users = await sync_to_async(User.objects.filter)(referrer=pk)
        serializer = aUserViewSerializer(users, many=True, context={'request': request})
        d = await sync_to_async(serializer.to_representation)(users)
        return Response(status=200, data=d)


class ReferralEmailSenderView(aAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None
    @extend_schema(summary="Actual users referral to email")
    def get(self, request):
        try:
            send_referral_code_to_email_for_current_user(request.user)
        except ObjectDoesNotExist as e:
            return Response(status=HTTP_404_NOT_FOUND, data=e.args)
        return Response(status=HTTP_200_OK)