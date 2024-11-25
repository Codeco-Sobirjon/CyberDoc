from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.account.models import CustomUser
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(UserAdmin):

    def group_names(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    model = CustomUser
    list_display = ('phone', 'email', 'first_name', 'last_name', 'surname', 'city', 'name_of_study', 'position',
                    'is_staff', 'group_names')
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

admin.site.site_header = _("CyberDoc Администрации Панель. ")
admin.site.site_title = _("CyberDoc Панель управления.")
admin.site.index_title = _("Добро пожаловать в админку CayberDoc.")
