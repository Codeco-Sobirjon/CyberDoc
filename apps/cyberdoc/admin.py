from django.contrib import admin
from apps.cyberdoc.models import (
    TypeConsultation, QualificationAuthor,
    Shrift, Guarantee, OrderWork, OrderWorkReview, DescribeProblem, OrderWorkFiles,
    Portfolio
)


class TypeConsultationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class QualificationAuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ShriftAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class GuaranteeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class OrderWorkFilesInlenes(admin.TabularInline):
    model = OrderWorkFiles
    fields = ['id', 'file']


class OrderWorkAdmin(admin.ModelAdmin):
    list_display = ('number_of_order', 'item', 'theme', 'deadline', 'author')
    search_fields = ('number_of_order', 'item', 'theme')
    list_filter = ('type_cons', 'qualification_author', 'shrift', 'guarantee', 'deadline')
    inlines = [OrderWorkFilesInlenes]


@admin.register(OrderWorkReview)
class OrderWorkReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_work', 'rating', 'text', 'created_at')
    list_filter = ('rating', 'user', 'order_work')
    search_fields = ('user__username', 'order_work__item', 'text')
    ordering = ('-rating',)


@admin.register(DescribeProblem)
class DescribeProblemAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ['user']
    search_fields = ('user__username',)


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'name',  'created_at', 'id')
    search_fields = ['name']


admin.site.register(TypeConsultation, TypeConsultationAdmin)
admin.site.register(QualificationAuthor, QualificationAuthorAdmin)
admin.site.register(Shrift, ShriftAdmin)
admin.site.register(Guarantee, GuaranteeAdmin)
admin.site.register(OrderWork, OrderWorkAdmin)
