from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from django.utils.safestring import mark_safe

# Register your models here.
class CustomUserAmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'date_of_birth',
                'profile_photo'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        (_('Important dates'), {'fields': (
            'last_login',
            'date_joined'
        )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'date_of_birth',
                'profile_photo',
                'is_staff',
                'is_active'
            ),
        }),
    )

    readonly_fields = ['profile_photo_preview']

    def profile_photo_preview(self, obj):
        if obj.profile_photo:
            return mark_safe(f'<img src="{obj.profile_photo.url}" width="100" height="100"/>')
        return _("No profile photo")

    profile_photo_preview.short_description = _("Profile Photo Preview")

admin.site.register(CustomUser, CustomUserAmin)
    


