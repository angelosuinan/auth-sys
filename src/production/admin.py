from django.contrib import admin
from .models import Harvest


class ProductionAdmin(admin.ModelAdmin):
    list_display = (
        'fish',
        'date_listed',
        'employee_attended',
        'quantity'
    )
    list_filter = [
        'fish',
        'date_listed',
        'employee_attended',
        'quantity'
           ]
    search_fields = (
        'fish',
        'date_listed'
            )
    readonly_fields = (
            )


admin.site.register(Harvest, ProductionAdmin)
