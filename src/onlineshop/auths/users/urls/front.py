from django.urls import path

from onlineshop.auths.users.views.front import RequestOTPView, VerifyOTPRequestView

urlpatterns=[
    path('login/',RequestOTPView.as_view()),
    path('verify/',VerifyOTPRequestView.as_view()),
]