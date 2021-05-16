# date_from = '2021-05-07'
# date_to = '2021-05-09'
# i = 1
# if i == 0:
#     date_domain = "and stock_move.date::DATE <= '%s'::DATE" % (date_to)

# elif i ==1:
#     date_domain = "and stock_move.date::DATE >= '%s'::DATE and stock_move.date::DATE <= '%s'::DATE" % (date_from,date_to)
# else:
#     date_domain = "and stock_move.date::DATE < '%s'::DATE" % (date_from)
# sql ='''
#         SELECT a.product_id as product_id, COALESCE(qty_in,0) -  COALESCE(qty_out,0) as qty, COALESCE(cost_in,0) -  COALESCE(cost_out,0) as cost,COALESCE(qty_in,0) as qty_in, COALESCE(qty_out,0) as qty_out,COALESCE(cost_in,0) as cost_in,COALESCE(cost_out,0) as cost_out from
#                 (SELECT product_id as product_id,COALESCE(sum(product_qty),0) as qty_in, COALESCE(sum(product_qty * price_unit),0) as cost_in, 1 as picking_type_id
#                         from stock_move,stock_picking 
#                         where stock_move.picking_id = stock_picking.id 
#                                 %(date_domain)s
#                         GROUP BY product_id) as a 
#                 LEFT JOIN 
#                 (SELECT product_id as product_id,COALESCE(sum(product_qty),0) as qty_out, COALESCE(sum(product_qty * price_unit),0) as cost_out, 4 as picking_type_id
#                         from stock_move,stock_picking 
#                         where stock_move.picking_id = stock_picking.id 
#                                 %(date_domain)s
#                         GROUP BY product_id) as b
#         on a.product_id = b.product_id
#         '''% ({'date_domain':date_domain,
#                 })
#             # logging.info(sql)

# print ('**sql**', sql)

# from datetime import date, datetime
# import time
# t = date.today()
# n = datetime.now()
# # dt = datetime.combine(date.today(), datetime.min.time())
# # dt = datetime.combine(date.today(),time.strptime('00:00','%H:%M'))
# dt = datetime.combine(date.today(),datetime.strptime('07:00','%H:%M').time())

# # print (dt, datetime.min.time())
# # print (dt > n)
# print (dt)
# r.shift_id.date


# r_shift_id_date = date(2021,5,9)
# r_date_begin = datetime(2021,5,10,10,0,0)
# shift_dt = datetime.combine(r_shift_id_date, datetime.min.time())
# print ('**r_date_begin**', r_date_begin, 'shift_dt', shift_dt)
# delta = r_date_begin - shift_dt
# delta_minutes = delta.days
# print (delta_minutes)

from datetime import datetime, date, timedelta
import pytz
input_date = date.today()
begin_hour = '07:30'
dt = datetime.combine(input_date, datetime.strptime(begin_hour,'%H:%M').time())
# utc_timezone = pytz.timezone('UTC')
# hcm_timezone = pytz.timezone('GMT +7')
# dt = dt.replace(tzinfo=hcm_timezone)
# dt = dt.replace(tzinfo=hcm_timezone).astimezone(utc_timezone).replace(tzinfo=None)
dt = dt - timedelta(hours=7)
print (dt)