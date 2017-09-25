from django.contrib import admin
from .models import Invoice, Payment


class InvoiceAdmin(admin.ModelAdmin):
    def _payment_amount(self, obj):
        return obj.payment.amount
    _payment_amount.short_description = 'payment'

    def get_fishes(self, obj):
        print obj.orders.all()
        return ", ".join([str(f.fish) for f in obj.orders.all()])
    get_fishes.short_description = 'fishes'

    list_display = (
        'customer_name',
        'id',
        'employee',
        'get_fishes',
        'date_acquired',

        'gender',
        'address',
        'telephone',
        'region',
        'remarks'
    )
    list_filter = [
        'customer_name',
           ]
    search_fields = (
    )
    readonly_fields = (
    )


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'fish',
        'amount',
        'quantity',
        'free',
        'nature',
    )
    list_filter = [
        'free'
    ]


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Payment, PaymentAdmin)
