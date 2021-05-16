date_from = '2021-05-07'
date_to = '2021-05-09'
i = 1
if i == 0:
    date_domain = "and stock_move.date::DATE <= '%s'::DATE" % (date_to)

elif i ==1:
    date_domain = "and stock_move.date::DATE >= '%s'::DATE and stock_move.date::DATE <= '%s'::DATE" % (date_from,date_to)
else:
    date_domain = "and stock_move.date::DATE < '%s'::DATE" % (date_from)
sql ='''
        SELECT a.product_id as product_id, COALESCE(qty_in,0) -  COALESCE(qty_out,0) as qty, COALESCE(cost_in,0) -  COALESCE(cost_out,0) as cost,COALESCE(qty_in,0) as qty_in, COALESCE(qty_out,0) as qty_out,COALESCE(cost_in,0) as cost_in,COALESCE(cost_out,0) as cost_out from
                (SELECT product_id as product_id,COALESCE(sum(product_qty),0) as qty_in, COALESCE(sum(product_qty * price_unit),0) as cost_in, 1 as picking_type_id
                        from stock_move,stock_picking 
                        where stock_move.picking_id = stock_picking.id 
                                and stock_picking.picking_type_id = 1 
                                %(date_domain)s
                        GROUP BY product_id) as a 
                LEFT JOIN 
                (SELECT product_id as product_id,COALESCE(sum(product_qty),0) as qty_out, COALESCE(sum(product_qty * price_unit),0) as cost_out, 4 as picking_type_id
                        from stock_move,stock_picking 
                        where stock_move.picking_id = stock_picking.id 
                                and stock_picking.picking_type_id = 4 
                                %(date_domain)s
                        GROUP BY product_id) as b
        on a.product_id = b.product_id
        '''% ({'date_domain':date_domain,
                })
            # logging.info(sql)

print ('**sql**', sql)