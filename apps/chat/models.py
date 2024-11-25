from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Conversation(models.Model):
    initiator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name="convo_starter", verbose_name=_("Инициатор")
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name="convo_participant", verbose_name=_("Получатель")
    )
    start_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Время начала"))

    objects = models.Manager()

    class Meta:
        verbose_name = _("1. Беседа")
        verbose_name_plural = _("1. Беседы")


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name='message_sender', verbose_name=_("Отправитель")
    )
    text = models.CharField(
        max_length=200, blank=True, verbose_name=_("Текст")
    )
    attachment = models.FileField(
        blank=True, verbose_name=_("Вложение")
    )
    conversation_id = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, verbose_name=_("Идентификатор беседы")
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Время отправки")
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _("2. Сообщение")
        verbose_name_plural = _("2. Сообщения")
        ordering = ('-timestamp',)
