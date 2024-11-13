from django.db import models
from django.utils.translation import gettext as _


class Service(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('Заголовок'))
    image = models.ImageField(upload_to='service/', null=True, blank=True, verbose_name=_("Изображение"))
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Дата публикации")

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("1. Услуга")
        verbose_name_plural = _("1. Услуга")


class SubmitRequest(models.Model):
    full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Полное имя"))
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Телефон"))
    email = models.EmailField(verbose_name=_("Электронная почта"), null=True, blank=True)
    topic = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Тема работы"))
    deadline = models.DateField(blank=True, null=True, verbose_name=_("Срок сдачи"))
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Дата публикации")

    objects = models.Manager()

    def __str__(self):
        return f'{self.full_name} {self.topic}'

    class Meta:
        verbose_name = _("3. Отправить заявку")
        verbose_name_plural = _("3. Отправить заявку")


class ServiceBlog(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Название"))
    text = models.TextField(null=True, blank=True, verbose_name=_("Текст"))
    url = models.URLField(null=True, blank=True, verbose_name=_("Ссылка"))
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name=_("Дата публикации"))

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("2. Блог услуги")
        verbose_name_plural = _("2. Блоги услуг")