from django.contrib import admin
from .models import Employee, Session
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()

    def _username(self, obj):
        uid = obj.get_decoded()['_auth_user_id']
        emp = User.objects.get(id=uid)
        return emp
    list_display = ['_username', 'session_key', '_session_data', 'expire_date']


class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
    
            )
    list_filter = (

           )
    search_fields = (
            )
    readonly_fields = (
            )


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Session, SessionAdmin)
