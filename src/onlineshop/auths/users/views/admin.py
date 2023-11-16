from rest_framework.authtoken.views import ObtainAuthToken

from onlineshop.auths.users.serializers.admin import UserAdminSerializer


class UserAdminView(ObtainAuthToken):
    serializer_class = UserAdminSerializer