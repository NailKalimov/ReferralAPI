from django.urls import path
from .views import ReferralListView, ReferralsCreate, ReferralDelete

urlpatterns = [
    path('all/', ReferralListView.as_view()),
    path('create/', ReferralsCreate.as_view()),
    path('delete/', ReferralDelete.as_view()),

]