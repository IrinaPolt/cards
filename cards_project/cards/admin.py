from django.contrib import admin

from .models import Card, Operation


class OperationInline(admin.TabularInline):
    model = Operation


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        'series',
        'number',
        'type',
        'validity_period',
        'status',
        'payout')
    search_fields = ('type', 'validity_period', 'status')
    list_filter = ('type', 'validity_period', 'status')
    inlines = [OperationInline, ]
