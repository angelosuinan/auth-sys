from import_export.admin import ImportExportModelAdmin
from daterange_filter.filter import DateRangeFilter
from .models import Invoice, Payment, Customer
from .resources import InvoiceResource
from django.contrib import admin


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'id',
        'gender',
        'address',
        'telephone',
        'region',
    )
    list_filter =[
        'region'
    ]


class InvoiceAdmin(ImportExportModelAdmin):
    resource_class = InvoiceResource

    def save_model(self, request, obj, form, change):
        obj.total_price = 0
        super(InvoiceAdmin, self).save_model(request, obj, form, change)
        total_price = 0

        for query in obj.orders.all():
            total_price += query.amount
            total_price = query.amount
        obj.total_price = total_price
        super(InvoiceAdmin, self).save_model(request, obj, form, change)

    def _payment_amount(self, obj):
        return obj.payment.amount
    _payment_amount.short_description = 'payment'

    def get_fishes(self, obj):
        return "\n".join([str(f.fish)+"-"+str(f.quantity) for f in obj.orders.all()])
    get_fishes.short_description = 'fishes'

    def get_customer_name(self, obj):
        return obj.customer.name
    get_customer_name.short_description = 'Name'

    def get_customer_gender(self, obj):
        return obj.customer.gender
    get_customer_gender.short_description = 'Gender'

    def get_customer_address(self, obj):
        return obj.customer.address
    get_customer_address.short_description = 'Address'

    def get_customer_telephone(self, obj):
        return obj.customer.telephone
    get_customer_telephone.short_description = 'telephone'

    def get_customer_region(self, obj):
        return obj.customer.region
    get_customer_region.short_description = 'region'

    def get_customer_organization(self, obj):
        return obj.customer.organization
    get_customer_organization.short_description = 'organization'

    def get_orders_free(self, obj):
        total = 0
        for payment in obj.orders.all():
            if payment.free:
                total += payment.free
        return total
    get_orders_free.short_description = 'FREE'

    def get_orders_nature(self, obj):
        concatted = ''
        for payment in obj.orders.all():
            if payment.nature:
                concatted += payment.nature + "\n"
        return concatted[:-2]
    get_orders_nature.short_description = 'NATURE'

    list_display = (
        'id',
        'date_acquired',
        'get_customer_name',
        'get_customer_gender',
        'get_customer_organization',
        'get_customer_address',
        'get_customer_region',
        'employee',
        'get_fishes',
        'total_price',
        'get_orders_free',
        'get_orders_nature',
        'remarks',
    )
    list_filter = (
        'orders__fish__name',
        'date_acquired',
        ('date_acquired', DateRangeFilter),
    )
    search_fields = ('customer__name',
    )
    readonly_fields = ('total_price', 'customer', 'orders' )


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'fish',
        'id',
        'amount',
        'quantity',
        'free',
        'nature',
    )
    list_filter = [
        'fish',
    ]
    search_fields = ('id',
    )


class CustomerAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        print type(obj.name)
        obj.save()
    list_display = (
        'name',
        'organization',
        'address',
        'gender',
        'telephone',
        'region'
    )
    list_filter = [
        'region',
    ]
    search_fields=('name', 'organization',)



admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Customer, CustomerAdmin)
