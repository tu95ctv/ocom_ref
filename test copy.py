import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta
date_in_feb = datetime.datetime(2013, 2, 21)
print ('*date_in_feb', date_in_feb)
print(datetime.datetime(2013, 2, 21) + relativedelta(day=31))  # End-of-month
# datetime.datetime(2013, 2, 28, 0, 0)