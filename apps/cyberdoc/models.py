import random
from django.db import models
from django.utils.translation import gettext as _

from apps.account.models import CustomUser


class TypeConsultation(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('Тип консультации'))

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("1. Тип консультации")
        verbose_name_plural = _("1. Типы консультаций")


class QualificationAuthor(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('Квалификация автора'))

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("2. Квалификация автора")
        verbose_name_plural = _("2. Квалификации авторов")


class Shrift(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('Шрифт'))

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("3. Шрифт")
        verbose_name_plural = _("3. Шрифты")


class Guarantee(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('Гарантия'))

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("4. Гарантия")
        verbose_name_plural = _("4. Гарантии")


class OrderWork(models.Model):
    number_of_order = models.CharField(max_length=250, null=False, blank=False, verbose_name=_("Номер заказа"))
    type_cons = models.ForeignKey(
        TypeConsultation, on_delete=models.CASCADE, null=False, blank=False,
        verbose_name=_("Тип консультации"), related_name="order_type_conf"
    )
    item = models.CharField(max_length=250, null=False, blank=False, verbose_name=_("Предмет"))
    theme = models.CharField(max_length=250, null=False, blank=False, verbose_name=_("Тема"))
    min_page_size = models.IntegerField(default=0, null=False, blank=False, verbose_name=_("Минимальный объем страниц"))
    number_of_sources_literature = models.IntegerField(default=0, null=False, blank=False, verbose_name=_("Количество источников литературы"))
    deadline = models.DateField(null=True, blank=True, verbose_name=_("Срок выполнения"))
    qualification_author = models.ForeignKey(
        QualificationAuthor, on_delete=models.CASCADE, null=False, blank=False,
        verbose_name=_("Квалификация автора"), related_name="order_qualification_author"
    )
    shrift = models.ForeignKey(
        Shrift, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=_("Шрифт"), related_name="order_shrift"
    )
    guarantee = models.ForeignKey(
        Guarantee, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=_("Гарантия"), related_name="order_guarantee"
    )
    text = models.TextField(null=True, blank=True, verbose_name=_("Текст"))

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name="Автор заказа", related_name="order_user")
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name=_("Дата публикации"))

    objects = models.Manager()

    def __str__(self):
        return self.item

    def generate_order_number(self):
        return f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(100, 999)}"

    def save(self, *args, **kwargs):
        if not self.number_of_order:
            self.number_of_order = self.generate_order_number()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("5. Заказ на работу")
        verbose_name_plural = _("5. Заказы на работу")


class OrderWorkFiles(models.Model):
    order_work = models.ForeignKey(
        OrderWork, on_delete=models.CASCADE, null=False, blank=False,
        verbose_name=_("Заказ на работу"), related_name="order_work_file"
    )
    file = models.FileField(upload_to='order_work/', null=True, blank=True, verbose_name=_("Файл"))

    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name=_("Дата публикации"))

    objects = models.Manager()

    def __str__(self):
        return self.order_work


class OrderWorkReview(models.Model):
    rating = models.IntegerField(
        null=False, blank=False, verbose_name=_("Оценка")
    )
    text = models.TextField(null=True, blank=True, verbose_name=_("Отзыв"))
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=False, blank=False,
        verbose_name=_("Пользователь"), related_name="order_reviews"
    )
    order_work = models.ForeignKey(
        OrderWork, on_delete=models.CASCADE, null=False, blank=False,
        verbose_name=_("Заказ на работу"), related_name="reviews"
    )
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name=_("Дата публикации"))

    objects = models.Manager()

    def __str__(self):
        return f"Отзыв пользователя {self.user} на заказ {self.order_work}"

    class Meta:
        verbose_name = _("6. Отзыв на заказ на работу")
        verbose_name_plural = _("6. Отзывы на заказы на работу")
        ordering = ['-rating']


class DescribeProblem(models.Model):
    text = models.TextField(null=True, blank=True, verbose_name=_("Текст"))
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=False, blank=False,
        verbose_name=_("Пользователь"), related_name="user_problem"
    )

    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name=_("Дата публикации"))

    objects = models.Manager()

    def __str__(self):
        return f"пользователя {self.user} : {self.created_at}"

    class Meta:
        verbose_name = _("Описание проблемы")
        verbose_name_plural = _("Описания проблем")
