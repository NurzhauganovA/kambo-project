from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PinToken


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'email', 'last_name', 'grade', 'address', 'is_active')
    search_fields = ('id', 'email', 'last_name', 'first_name', 'phone_number')

    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "avatar",
                    "language",
                    "username",
                    "address",
                    "about_yourself"
                )
            }
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_admin",
                ),
            },
        ),
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "created_at",
                )
            }
        ),
    )
    readonly_fields = ('created_at',)


@admin.register(PinToken)
class PinTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'code', 'expiration', 'is_accepted', 'is_expired')
    ordering = ('id',)
