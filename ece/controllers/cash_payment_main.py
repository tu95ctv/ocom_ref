# -*- coding: utf-8 -*-
import logging
import pprint
import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class TransferController(http.Controller):
    _accept_url = '/payment/cash/feedback'

    @http.route([
        '/payment/cash/feedback',
    ], type='http', auth='public', csrf=False)
    def transfer_form_feedback(self, **post):
        # print (haha)
        post
        _logger.info('Beginning form_feedback with post data %s', pprint.pformat(post))  # debug
        request.env['payment.transaction'].sudo().form_feedback(post, 'transfer')
        return werkzeug.utils.redirect('/payment/process')
        # return werkzeug.utils.redirect('/shop/confirmation')

