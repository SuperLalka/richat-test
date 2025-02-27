
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from app.users.models import UserBasket

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (
            _('Important dates'),
            {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            }
        ),
    )
    list_display = ['email', 'username', 'is_staff', 'is_superuser']
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ['name']
    ordering = ['id']
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            },
        ),
    )


@admin.register(UserBasket)
class UserBasketAdmin(admin.ModelAdmin):
    list_display = ['user', 'items_list']
    list_display_links = list_display[:2]
    raw_id_fields = ['user']

    @admin.display(description='items')
    def items_list(self, obj) -> str:
        return format_html('<br>'.join(obj.items.values_list('stripe_obj_id', flat=True)))
