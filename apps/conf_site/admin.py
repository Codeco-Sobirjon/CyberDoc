from django.contrib import admin
from apps.conf_site.models import Service, SubmitRequest, ServiceBlog


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'id')
    search_fields = ('title',)
    list_filter = ('title',)
    ordering = ('title',)


@admin.register(SubmitRequest)
class SubmitRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'topic', 'deadline', 'created_at', 'id')
    search_fields = ('full_name', 'email', 'topic')
    list_filter = ['deadline']
    ordering = ('-created_at',)
    date_hierarchy = 'deadline'


@admin.register(ServiceBlog)
class ServiceBlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'url')
    search_fields = ('name', 'text')
    list_filter = ('created_at',)
    ordering = ('-created_at',)