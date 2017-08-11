from datetime import datetime


class Helper(object):

    def time_diff(self, time_in_am, time_out_am):
        FMT = '%H:%M:%S'
        time_diff_am = datetime.strptime(str(time_out_am), FMT) - datetime.strptime(str(time_in_am), FMT)
        ftr = [3600, 60, 1]
        difference = sum([a*b for a, b in zip(ftr, map(int, str(time_diff_am).split(':')))])
        if difference < 300:
            return True
        return False
