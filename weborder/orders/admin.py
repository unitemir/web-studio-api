from django.contrib import admin
from .models import Order
from .tasks import process_order


def process_selected_orders(modeladmin, request, queryset):
    for order in queryset:
        process_order.delay(order.id)

process_selected_orders.short_description = "Process selected orders through Celery"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'created_at', 'status')
    actions = [process_selected_orders]
