from django.contrib import admin
from .models import Order, Payment


class OrderAdmin(admin.ModelAdmin):
    def _payment_amount(self, obj):
        return obj.payment.amount
    _payment_amount.short_description = 'payment'

    def get_fishes(self, obj):
        print obj.payment.all()
        return ", ".join([str(f.fish) for f in obj.payment.all()])
    get_fishes.short_description = 'fishes'

    list_display = (

        'employee',
        'get_fishes',
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


<<<<<<< Updated upstream
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
=======
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'fish',
>>>>>>> Stashed changes
        'amount',
        'free',
        'nature',
    )
    list_filter = [
        'free',
    ]


admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
