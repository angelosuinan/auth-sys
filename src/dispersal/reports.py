from django.http import HttpResponse
import csv


class Report(object):
    filename = ""

    def __init__(self, year, order, fishes):
        self.year = year
        self.order = order
        self.fishes = fishes
        self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
            'September', 'October', 'November', 'December', 'Total']
        self.quarterly = ['Q1', 'Q2', 'Q3', 'Q4', 'Total']
        self.months_range = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        self.to_csv = []

    def parse(self, points):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="'+str(self.fishes)+'.csv"'


        writer = csv.writer(response)

        li = ['Fishes'] + self.months
        writer.writerow(li)
        for point, fish in zip(points, self.fishes):
            the_list = []
            the_list.append(fish)
            for p in point:
                the_list.append(p)
            writer.writerow(the_list)

        return response

    def quarterly(self):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        writer = csv.writer(response)
        writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
        writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    def get_headers(self,):
        if self.order == 'monthly':
            return self.months
        return self.quarterly

    def sample(self, queryset, field):
        points = []

        for fish in self.fishes:
            fish_quantity = []
            fish_csv = [fish]
            for month in self.months_range:
                query = queryset.filter(date_acquired__month=month)
                invoice_total = 0
                for invoice in query:
                    orders_total = 0
                    for order in invoice.orders.all():

                        if fish == order.fish.name:
                            orders_total += order.quantity + order.free
                    invoice_total += orders_total

                fish_quantity.append(invoice_total)
            points.append(fish_quantity)
        average = [float(sum(l))/len(l) for l in zip(*points)]
        average = sum(average) / float(len(average))

        return points, int(average/2)