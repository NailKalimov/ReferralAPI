from adrf.serializers import ModelSerializer

from .models import Referral


class ReferralSerializer(ModelSerializer):
    class Meta:
        model = Referral
        fields = '__all__'