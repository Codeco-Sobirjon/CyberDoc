from django.contrib import admin
from apps.chat.models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 1
    fields = ('sender__phone', 'text', 'attachment', 'timestamp')
    readonly_fields = ('timestamp',)
    verbose_name = "Сообщение"
    verbose_name_plural = "Сообщения"


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('initiator', 'receiver', 'start_time')
    list_filter = ('start_time',)
    search_fields = ('initiator__username', 'receiver__username')
    inlines = [MessageInline]
    verbose_name = "Беседа"
    verbose_name_plural = "Беседы"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'conversation_id', 'text', 'timestamp')
    list_filter = ('timestamp', 'conversation_id')
    search_fields = ('sender__username', 'text')
    verbose_name = "Сообщение"
    verbose_name_plural = "Сообщения"
