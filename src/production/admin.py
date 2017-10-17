from import_export.admin import ImportExportModelAdmin
from daterange_filter.filter import DateRangeFilter
from resources import HarvestResource
from django.contrib import admin
from models import Harvest, AreaHarvested
# Register your models here.


@admin.register(Harvest)
class HarvestAdmin(ImportExportModelAdmin):
    resource_class = HarvestResource

    def _fish_name(self,obj):
        return obj.fish.name
    _fish_name.short_description = 'fish'

    list_display = (
        '_fish_name',
        'id',
        'quantity',
        'date_listed',
        'employee_attended',
        'remarks',
    )
    list_filter = (
        'fish__name',
        'date_listed',
        'id',
        ('date_listed', DateRangeFilter),
    )
    search_fields = (
    )
    readonly_fields = ()


@admin.register(AreaHarvested)
class AreaHarvestedAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    search_fields = (
        ('name',)
    )
    readonly_fields = ()
