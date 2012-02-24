from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User

from proto.accounts.models import UserProfile
from proto.common.admin import FileBrowseField


class UserProfileAdminForm(forms.ModelForm):
    avatar = FileBrowseField(required=not UserProfile._meta.get_field('avatar').blank)

    class Meta:
        model = UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    form = UserProfileAdminForm
    max_num = 1
    can_delete = False


class UserAdmin(AuthUserAdmin):
    inlines = [UserProfileInline]


# Unregister default user admin
admin.site.unregister(User)
# Register new user admin
admin.site.register(User, UserAdmin)
