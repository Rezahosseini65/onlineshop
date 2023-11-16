from django.urls import path

from onlineshop.auths.users.views.admin import UserAdminView

urlpatterns = [
    path('login/',UserAdminView.as_view()),
]