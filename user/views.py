from copy import copy
from django.contrib.auth import get_user_model
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserViewSerializer, UserCreateSerializer
from rest_framework import generics


@extend_schema_view(
    retrieve=extend_schema(summary="User detail"),
    list=extend_schema(summary="List of users")
)
class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    User = get_user_model()
    serializer_class = UserViewSerializer
    queryset = User.objects.all()
    # permission_classes = [permissions.IsAuthenticated]


class ReferralUserCreate(APIView):
    serializer_class = UserCreateSerializer

    @extend_schema(
        summary="New user",
        examples=[
            OpenApiExample(
                "Post example",
                value={
                    "username": "testuser_xxx",
                    "email": "user@example.com",
                    "password": "string",
                    "referrer": None
                }
            )
        ]
    )
    def post(self, request, ref_code=None):
        data = copy(request.data)
        if ref_code:
            data['referrer'] = get_object_or_404(User, referral_code__code=ref_code).id
        serializer = UserCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED,
                            data="User registered successfully")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReferralUserListView(APIView):
    serializer_class = UserViewSerializer

    @extend_schema(summary="List of invited users")
    def get(self, request, pk):
        users = User.objects.filter(referrer=pk)
        serializer = UserViewSerializer(users, many=True, context={'request': request})
        return Response(status=200, data=serializer.data)
