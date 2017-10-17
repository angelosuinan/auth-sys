from django.http import HttpResponse
from models import Invoice
from production.models import Harvest
import csv


class Stocks(object):
    filename = ""

    def __init__(self, year, order, fish):
        self.year = year
        self.order = order
        self.fish = fish
        self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
            'September', 'October', 'November', 'December', 'Total']
        self.quarterly = ['Q1', 'Q2', 'Q3', 'Q4', 'Total']
        self.months_range = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        self.quarterly_range = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        self.to_csv = []

    def get_headers(self,):
        if self.order == 'monthly':
            return self.months
        return self.quarterly

    def charts(self,):
        points = []
        average = 0
        year = self.year
        fish = self.fish
        order = self.order
        invoices = Invoice.objects.filter(date_acquired__year=year,)
        harvests = Harvest.objects.filter(date_listed__year=year,)

        invoice_list = []
        harvest_list = []

        if order == "monthly":
            intervals = self.months_range
        order = self.quarterly_range
        for interval in intervals:
            invoice_query = invoices.filter(date_acquired__month=interval,)
            harvest_query = harvests.filter(date_listed__month=interval,)

            invoice_total = 0
            for invoice in invoice_query:
                orders_total = 0
                for order in invoice.orders.all():
                    if fish == order.fish.name:
                        orders_total += order.quantity
                        if order.free:
                            orders_total += order.free
                invoice_total += orders_total
            invoice_list.append(invoice_total)

            harvest_total = 0
            for harvest in harvest_query.filter(fish__name=fish):
                harvest_total += harvest.quantity
            harvest_list.append(harvest_total)
        points.append(invoice_list)
        points.append(harvest_list)
        average = map(max, points)
        average = max(average) / 10
        return points, int(average)

    def export(self, points):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="'+str(self.fish)+'.csv"'

        writer = csv.writer(response)

        li = ['Fish'] + self.months
        writer.writerow(li)

        li = ["Fish Dispersal"]
        writer.writerow(li)

        total_dispersal = sum(points[0])
        points[0].insert(0, self.fish)
        points[0].append(total_dispersal)
        writer.writerow(points[0])

        li = ["Fish Production"]
        writer.writerow(li)
        total_harvest = sum(points[1])
        points[1].insert(0, self.fish)
        points[1].append(total_harvest)
        writer.writerow(points[1])

        return response
