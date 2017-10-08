from django.contrib import admin
from .models import Fish, Category


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


class CategoryAdmin(admin.ModelAdmin):
    def get_fishes(self, obj):
        fishes = Fish.objects.filter(category=obj)
        sorted_fish = ''
        for fish in fishes:
            print fish.name
            sorted_fish += fish.name + ', '
        return sorted_fish
    get_fishes.short_description = 'fishes'

    list_display = (
        'id',
        'name',
        'get_fishes'
    )


admin.site.register(Fish, FishAdmin)
admin.site.register(Category, CategoryAdmin)
