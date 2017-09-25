from django.contrib import admin
from .models import Attendance
from django.contrib import messages
from .utils import Helper


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">bubble_chart</i>'

    def get_actions(self, request):
        actions = super(AttendanceAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    list_display = (
            'date',
            'employee',
            'time_in_am',
            'time_out_am',
            'time_in_pm',
            'time_in_pm',
            'total_time',
            'modified_time'
            )
    list_filter = [
            'employee',
            'date',
           ]
    search_fields = (
            'date',
            )
    readonly_fields = ('total_time', )
