from django.contrib import admin
from .models import Invoice, Order


class InvoiceAdmin(admin.ModelAdmin):
    def _payment_amount(self, obj):
        return obj.payment.amount
    _payment_amount.short_description = 'payment'

    list_display = (
        '_payment_amount',
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


class OrderAdmin(admin.ModelAdmin):
    def get_fishes(self, obj):
        return "\n".join([str(f) for f in obj.fish.all()])

    list_display = (
        'get_fishes',
        'amount',
        'free',
        'nature',
    )
    list_filter = [
        'free',
    ]


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Order, OrderAdmin)
