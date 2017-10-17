from .models import Invoice, Payment, Customer
from import_export import resources, fields
from django.contrib.auth.models import User


class InvoiceResource(resources.ModelResource):
    Date = fields.Field()
    Name = fields.Field()
    Gender = fields.Field()
    Organization = fields.Field()
    Address = fields.Field()
    Quantity = fields.Field()
    Total_Quantity = fields.Field()
    Region = fields.Field()
    Employee_attended = fields.Field()
    Fishes = fields.Field()
    Free = fields.Field()
    Nature = fields.Field()

    class Meta:
        model = Invoice
        fields = (
            'invoice_number', 'Date', 'Name', 'Gender', 'Address', 'Region',
            'Employee_attended', 'Fishes', 'total_price', 'Free', 'Nature',
            'remarks',
        )
        export_order = (
            'invoice_number', 'Date', 'Name', 'Gender', 'Organization', 'Address', 'Region',
            'Employee_attended', 'Fishes', 'Quantity', 'Total_Quantity', 'total_price', 'Free', 'Nature',
            'remarks',
        )

    def dehydrate_Date(self, invoice):
        return '%s' % (invoice.date_acquired, )

    def dehydrate_Name(self, invoice):
        return '%s' % (invoice.customer.name, )

    def dehydrate_Gender(self, invoice):
        customer = invoice.customer

        return '%s' % (customer.get_gender_display(), )

    def dehydrate_Organization(self, invoice):
        return '%s' % (invoice.customer.organization, )

    def dehydrate_Address(self, invoice):
        return '%s' % (invoice.customer.address, )

    def dehydrate_Region(self, invoice):
        return '%s' % (invoice.customer.get_region_display(), )

    def dehydrate_Employee_attended(self, invoice):
        first_name = invoice.employee.first_name
        last_name = invoice.employee.last_name
        return '%s %s' % (first_name, last_name)

    def dehydrate_Fishes(self, invoice):
        fishes = ''
        for payment in invoice.orders.all():
            fishes += '%s\n' % ( payment.fish)
        return fishes

    def dehydrate_Quantity(self, invoice):
        fishes = ''
        for payment in invoice.orders.all():
            fishes += '%s\n' % (payment.quantity)
        return fishes

    def dehydrate_Total_Quantity(self, invoice):
        total = 0
        for payment in invoice.orders.all():
            total += payment.quantity
        return total

    def dehydrate_Free(self, invoice):
        total_free = 0
        for payment in invoice.orders.all():
            if payment.free:
                total_free += payment.free
        return total_free

    def dehydrate_Nature(self, invoice):
        natures = ''
        for payment in invoice.orders.all():
            natures += '%s\n' % (payment.nature)
        return natures
