from django.contrib import admin
from .models import Fish


class FishAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'scientific_name'
    )
    list_filter = [
           ]
    search_fields = (
        'name',
            )
    readonly_fields = (
            )


admin.site.register(Fish, FishAdmin)
