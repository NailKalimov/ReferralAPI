from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, ReferralUserCreate, ReferralUserListView

router = routers.DefaultRouter()
router.register(r'all_users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('register/', ReferralUserCreate.as_view()),
    path('register/<str:ref_code>', ReferralUserCreate.as_view()),
    path('referrals/<int:pk>', ReferralUserListView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]