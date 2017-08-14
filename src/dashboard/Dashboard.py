from controlcenter import Dashboard, widgets
from employee.models import EmployeeProfile


class ModelItemList(widgets.ItemList):
    model = EmployeeProfile
    list_display = ('pk', 'contact_number')


class MyDashboard(Dashboard):
    widgets = (
        ModelItemList,
    )
