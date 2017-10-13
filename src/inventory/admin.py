from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from django.contrib import admin
from .models import Item
from django.contrib import messages


def get_total(modeladmin, request, queryset):
    total_amount = 0
    for obj in queryset:
        total_amount += obj.amount
    messages.success(request, str(total_amount) + " php")
get_total.short_description = "Get total of mark item/s"


class BookResource(resources.ModelResource):

    class Meta:
        model = Item
        fields = ('id', 'name', 'amount', 'description', 'date_acquired')
        export_order = (
            'id', 'name', 'amount', 'description', 'date_acquired'
        )


class DispersalAdmin(ImportExportModelAdmin):
    resource_class = BookResource
    list_display = (
        'name',
        'amount',
        'description',
        'employee',
        'date_acquired',
    )
    list_filter = [
        'employee',
        'name',
        'date_acquired'
           ]
    search_fields = (
            )
    readonly_fields = (
            )
    actions = [
        get_total
    ]


admin.site.register(Item, DispersalAdmin)
