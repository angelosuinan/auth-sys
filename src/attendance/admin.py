from import_export.admin import ImportExportModelAdmin
from daterange_filter.filter import DateRangeFilter
from django.db.models.query import QuerySet
from import_export import resources, fields
from django.contrib import admin
from .models import Attendance
from django.contrib import messages
from .utils import Helper
import tablib
from datetime import time


class BookResource(resources.ModelResource):

    class Meta:
        model = Attendance
        fields = ('date', 'time_in_am', 'time_out_am', 'time_in_pm', 'time_out_pm',
        'extra_time_in', 'extra_time_out', 'total_time')
        # exclude = ('id', 'created_time', 'modified_time', 'active')

    @classmethod
    def field_from_django_field(self, field_name, django_field, readonly):
        """
        Returns a Resource Field instance for the given Django model field.
        """
        FieldWidget = self.widget_from_django_field(django_field)
        widget_kwargs = self.widget_kwargs_for_field(field_name)
        column_name = field_name.title()
        column_name = column_name.replace("_", " ")

        field = fields.Field(attribute=field_name, column_name=column_name,
                widget=FieldWidget(**widget_kwargs), readonly=readonly)

        return field


@admin.register(Attendance)
class AttendanceAdmin(ImportExportModelAdmin):
    icon = '<i class="material-icons">bubble_chart</i>'

    def get_actions(self, request):
        actions = super(AttendanceAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def save_model(self, request, obj, form, change):
        if obj.leave_of_absence:
            obj.time_in_am = time(8, 0, 0)
            obj.time_out_am = time(12, 0, 0)
            obj.time_in_pm = time(13, 0, 0)
            obj.time_out_pm = time(16, 0, 0)
        obj.save()
    resource_class = BookResource
    list_display = (
            'date',
            'id',
            'employee',
            'time_in_am',
            'time_out_am',
            'time_in_pm',
            'time_out_pm',
            'total_time',
            'modified_time'
            )
    list_filter = (
            'employee',
            'date',
            'active',
            'leave_of_absence',
            ('date', DateRangeFilter),
           )
    search_fields = (
            'date',
            )
    readonly_fields = ('total_time', )
