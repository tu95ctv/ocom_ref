
from odoo import http
import json
from odoo.http import Controller, route, request
from odoo.exceptions import UserError


class ABCcontroller(Controller):

    # @route('/odoo_api3/get',methods=['GET'], auth="public")
    @http.route('/odoo_api3/get/<string:model_name>', 
    methods=['POST','GET'],
    type='json',
    auth='none',
     )
    def getabc(self, **params):
        print ('**params**', params)
        result = {'model_name': params['model_name'], 
                'params':str(params)
            }
        return result
        # return json.dumps(result)

# class ABCcontrollerInherit(ABCcontroller):
#     # @route('/odoo_api3/get',methods=['GET'], auth="public")
#     # @http.route( auth='none', methods=['GET'], type='json')
#     @http.route()
#     def getabc(self,model_name, **params):
#         rs = super().getabc(model_name, **params)
#         rs.update({'123':'321'})
#         # raise ValueError('abc')
#         return rs   
#         # result = {'model_name': model_name, 
#         #         'params':str(params)
#         #     }
        # return json.dumps(result)