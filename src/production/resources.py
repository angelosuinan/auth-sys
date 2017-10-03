from models import Harvest
from import_export import resources, fields
from django.contrib.auth.models import User


class HarvestResource(resources.ModelResource):
    Fish = fields.Field()
    Quantity = fields.Field()
    Date = fields.Field()

    class Meta:
        model = Harvest
        fields = (
            'Fish', 'Quantity', 'Date',
        )
        export_order = (
            'Fish', 'Quantity', 'Date',
        )

    def dehydrate_Fish(self, harvest):
        return '%s' % (harvest.fish.name, )

    def dehydrate_Quantity(self, harvest):
        return '%s' % (harvest.quantity, )

    def dehydrate_Date(self, harvest):
        return '%s' % (harvest.date_listed, )
