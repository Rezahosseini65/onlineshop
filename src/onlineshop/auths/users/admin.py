from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from onlineshop.auths.users.models import MyUser, OTPrequest, Profile


# Register your models here.
@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    pass

admin.site.register(OTPrequest)
admin.site.register(Profile)