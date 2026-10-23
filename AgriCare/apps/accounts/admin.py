from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class AgriCareUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("AgriCare profile", {"fields": ("role", "phone_number", "preferred_language", "organization")}),
    )
    list_display = ("username", "email", "role", "phone_number", "is_staff")
    list_filter = UserAdmin.list_filter + ("role",)
