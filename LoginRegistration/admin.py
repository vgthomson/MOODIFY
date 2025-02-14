from .models import *
from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.models import User

admin.site.register(PasswordReset)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_deleted')
    list_filter = ('is_deleted',)
    actions = ['soft_delete', 'restore_user']

    def soft_delete(self, request, queryset):
        queryset.update(is_deleted=True)
        self.message_user(request, "Selected users have been soft deleted.")

    def restore_user(self, request, queryset):
        queryset.update(is_deleted=False)
        self.message_user(request, "Selected users have been restored.")

    soft_delete.short_description = "Soft Delete Selected Users"
    restore_user.short_description = "Restore Selected Users"

admin.site.register(UserProfile, UserProfileAdmin)
