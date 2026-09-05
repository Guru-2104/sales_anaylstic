from django.contrib import admin
from .models import Sale


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):

    list_display = (
        'order_id',
        'order_date',
        'customer_name',
        'product_name',
        'category',
        'region',
        'quantity',
        'sales_amount',
        'profit',
    )

    search_fields = (
        'order_id',
        'customer_name',
        'product_name',
    )

    list_filter = (
        'region',
        'category',
        'order_date',
    )