from adrf.generics import ListAPIView, CreateAPIView, DestroyAPIView, aget_object_or_404
from adrf.mixins import get_data
from asgiref.sync import sync_to_async
from django.utils.datetime_safe import datetime
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status, permissions
from rest_framework.response import Response

from .models import Referral
from .serializers import ReferralSerializer


class ReferralListView(ListAPIView):
    serializer_class = ReferralSerializer
    queryset = Referral.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class ReferralsCreate(CreateAPIView):
    serializer_class = ReferralSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(examples=[
        OpenApiExample("empty body", value={})
    ])
    async def acreate(self, request, *args, **kwargs):
        current_user = request.user
        active_code = await Referral.objects.filter(owner=current_user).afirst()
        print(active_code)
        if active_code:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            data="The current user has a referral code")
        serializer = self.get_serializer(data=request.data)
        await sync_to_async(serializer.is_valid)(raise_exception=True)
        await self.perform_acreate(serializer)
        data = await get_data(serializer)
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class ReferralDelete(DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReferralSerializer
    queryset = Referral.objects.all()

    async def aget_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        current_user = self.request.user
        print(current_user)
        obj = await aget_object_or_404(queryset, owner=current_user, end_date__gte=datetime.today())
        self.check_object_permissions(self.request, obj)
        return obj
