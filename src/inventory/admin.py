from django.contrib import admin
from .models import Item
from django.contrib import messages


def get_total(modeladmin, request, queryset):
    total_amount = 0
    for obj in queryset:
        total_amount += obj.amount
    messages.success(request, str(total_amount) + " php")
get_total.short_description = "Get total of mark item/s"


class DispersalAdmin(admin.ModelAdmin):
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
