from django.contrib import admin
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Profile


class MyProfileAdmin(Profile):
    form = MyUserChangeForm
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('nickname', 'avatar_path', )}),
    )


admin.site.register(Profile)
admin.site.register(MyProfileAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(LikeDislike)
