from django.utils.datetime_safe import datetime
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .models import Referral
from .serializers import ReferralSerializer


class ReferralListView(generics.ListAPIView):
    serializer_class = ReferralSerializer
    queryset = Referral.objects.all()


class ReferralsCreate(generics.CreateAPIView):
    serializer_class = ReferralSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        current_user = request.user
        active_code = Referral.objects.filter(owner=current_user).filter(end_date__gte=datetime.today())
        if active_code:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            data="The current user has a referral code")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReferralDelete(generics.DestroyAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReferralSerializer
    def get_queryset(self):
        current_user = self.request.user
        queryset = Referral.objects.filter(owner=current_user).filter(end_date__gte=datetime.today())
        return queryset
