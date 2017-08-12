from django.contrib import admin
from .models import EmployeeProfile, Session
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
    def _username(self, obj):
        return obj.user.username
    _username.short_description = 'username'

    def _fullname(self, obj):
        return obj.user.first_name + " " + obj.user.last_name
    _fullname.short_description = 'full name'

    def _lastlogin(self, obj):
        return obj.user.last_login
    _lastlogin.short_description = 'Last Login at'

    def _active(self, obj):
        return obj.user.is_active
    _active.short_description = 'active'

    list_display = (
            '_username',
            'position',
            '_fullname',
            '_active',
            '_lastlogin',
            )
    list_filter = (
            'position',
           )
    search_fields = (
            )
    readonly_fields = (
            )


admin.site.register(EmployeeProfile, EmployeeAdmin)
admin.site.register(Session, SessionAdmin)
