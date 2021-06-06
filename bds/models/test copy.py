# from inspect import getmembers, currentframe
# from operator import attrgetter, itemgetter

# class A():
#     b = 1

# rs = getmembers(A,lambda i:isinstance(i,int))
# print (rs)
from datetime import datetime,date
now = datetime.now()
today = date.today()
print (today.strftime('Ngày %d tháng %m năm %Y'))
# mmm1-dd-YYYY 
print (today.strftime('%b-%d-%Y'))

