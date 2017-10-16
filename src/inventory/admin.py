from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from django.contrib import admin
from .models import Item, Category
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


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        )


class DispersalAdmin(ImportExportModelAdmin):
    resource_class = BookResource
    list_display = (
        'name',
        'id',
        'description',
        'quantity',
        'unit',
        'amount',
        'category',
        'employee',
        'date_acquired',
    )
    list_filter = [
        'employee',
        'date_acquired',
        'category__name'
           ]
    search_fields = (
        'employee',
            )
    readonly_fields = (
        'property_number',
            )
    actions = [
        get_total
    ]


admin.site.register(Item, DispersalAdmin)
admin.site.register(Category, CategoryAdmin)
