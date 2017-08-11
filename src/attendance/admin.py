from django.contrib import admin
from .models import Attendance
from django.contrib import messages
from models import Employee
from .utils import Helper

helper = Helper()


class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
            'date',
            'employee',
            'time_in_am',
            'time_out_am',
            'time_in_pm',
            'time_in_pm',
            'notes',
            )
    list_filter = [
            'employee__user'
           ]
    search_fields = (
            )
    readonly_fields = (
            )


admin.site.register(Attendance, AttendanceAdmin)
