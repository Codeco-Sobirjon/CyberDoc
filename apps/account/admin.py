from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.account.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('phone', 'email', 'first_name', 'last_name', 'surname', 'city', 'name_of_study', 'position', 'is_staff')
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email', 'surname', 'city', 'name_of_study', 'position', 'avatar')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'first_name', 'last_name', 'email', 'surname', 'avatar', 'city', 'name_of_study', 'position', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('phone', 'surname', 'first_name', 'last_name', 'email')
    ordering = ('phone',)


admin.site.register(CustomUser, CustomUserAdmin)
