from django.contrib import admin
from django.utils.html import format_html

from app.items.models import Discount, Item, Order, Price, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'stripe_obj_id', 'name', 'description']
    list_display_links = list_display[:3]
    search_fields = ['id', 'stripe_obj_id']
    ordering = ['-id']


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ['id', 'stripe_obj_id', 'currency', 'unit_amount', 'product']
    list_display_links = list_display[:2]
    search_fields = ['id', 'stripe_obj_id']
    ordering = ['-id']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'items_list', 'discounts_list', 'taxes_list']
    list_display_links = list_display[:3]
    raw_id_fields = ['user', 'items', 'discounts', 'taxes']

    @admin.display(description='items')
    def items_list(self, obj) -> str:
        return format_html('<br>'.join(obj.items.values_list('stripe_obj_id', flat=True)))

    @admin.display(description='discounts')
    def discounts_list(self, obj) -> str:
        if obj.discounts:
            return format_html('<br>'.join(obj.discounts.values_list('name', flat=True)))
        return '-'

    @admin.display(description='taxes')
    def taxes_list(self, obj) -> str:
        if obj.taxes:
            return format_html('<br>'.join(obj.taxes.values_list('name', flat=True)))
        return '-'


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']
    list_display_links = list_display


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']
    list_display_links = list_display
