from django.contrib import admin
from files.models import Category, File
# Register your models here.


class FileAdmin(admin.ModelAdmin):
    def _username(self, obj):
        return obj.user.username
    _username.short_description = 'username'

    list_display = (
        'author',
        'upload',
        'category',
        'remarks',
            )
    list_filter = (
        'author',
        'created_time'
           )
    search_fields = (
        'name',
            )
    readonly_fields = (
            )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
            )


admin.site.register(File, FileAdmin)
admin.site.register(Category, CategoryAdmin)
