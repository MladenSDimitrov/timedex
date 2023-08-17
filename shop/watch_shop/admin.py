from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from shop.watch_shop.forms import SignUpForm, UserEditForm
from shop.watch_shop.models import Watch, Order, Address, OrderWatch

UserModel = get_user_model()


@admin.register(UserModel)
class UserAdmin(UserAdmin):
    form = UserEditForm
    add_form = SignUpForm
    model = UserModel

    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'email',
                    'password',
                ),
            }),
        (
            'Personal info',
            {
                'fields': (
                    'first_name',
                    'last_name',
                ),
            },
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (
            'Important dates',
            {
                'fields': (
                    'last_login',
                    'date_joined',
                ),
            },
        ),
    )
    add_fieldsets = (
                        (
                            None,
                            {
                                "classes": ("wide",),
                                "fields": ("email", "password1", "password2",),
                            },
                        ),
                    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


@admin.register(Address)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(Watch)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderWatch)
class OrderAdmin(admin.ModelAdmin):
    pass
