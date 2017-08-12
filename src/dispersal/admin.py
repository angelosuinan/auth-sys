from django.contrib import admin
from .models import Order, Payment


class OrderAdmin(admin.ModelAdmin):
    def _payment_amount(self, obj):
        return obj.payment.amount
    _payment_amount.short_description = 'payment'
    list_display = (
        '_payment_amount',
        'fish',
        'employee',
        'date_acquired',
        'customer_name',
        'gender',
        'address',
        'telephone',
        'region',
        'remarks'
    )
    list_filter = [
           ]
    search_fields = (
        'fish',
            )
    readonly_fields = (
            )


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'amount',
        'free',
        'nature',
    )
    list_filter = [
        'free',
    ]


admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
