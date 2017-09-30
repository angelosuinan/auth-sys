from import_export.admin import ImportExportModelAdmin
from daterange_filter.filter import DateRangeFilter
from resources import HarvestResource
from django.contrib import admin
from models import Harvest
# Register your models here.


@admin.register(Harvest)
class HarvestAdmin(ImportExportModelAdmin):
    resource_class = HarvestResource

    def _fish_name(self,obj):
        return obj.fish.name
    _fish_name.short_description = 'fish'

    list_display = (
        '_fish_name',
        'quantity',
        'date_listed',
        'employee_attended',
    )
    list_filter = (
        'fish__name',
        'date_listed',
        ('date_listed', DateRangeFilter),
    )
    search_fields = (
    )
    readonly_fields = ()
