import logging
_logger = logging.getLogger(__name__)
from odoo import http
from odoo.tools.translate import _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
import requests
from ast import literal_eval
import json
import werkzeug.utils
from werkzeug.exceptions import BadRequest
from odoo.service import common
import logging
import requests
from urllib.parse import urlencode
_logger = logging.getLogger(__name__)
from odoo.addons.payment_clictopay.models.currency import CURRENCY_CODE



class WebsiteSale(WebsiteSale):

    _paytabs_feedbackUrl = '/payment/clictopay/checkout'
    _return_url = '/clictopay/feedback'

    @http.route([_paytabs_feedbackUrl], type='json', auth='public', website=True)
    def clictopay_payment(self, **post):
        currency = post.get("currency")
        merchant_detail = request.env["payment.acquirer"].sudo().browse(int(post.get('acquirer',0)))
        request.session['so_id']= post.get("reference")
        total_amount = literal_eval(post.get('amount'))
        clictopay_tx_values = {
            'userName': merchant_detail.detail_clictopay_payment_acquire().get('Username'),
            'password': merchant_detail.detail_clictopay_payment_acquire().get('Password'),
            'returnUrl': merchant_detail.clictopay_url().get('return_url'),
            'orderNumber': post.get("reference"),
            'currency': int(CURRENCY_CODE.get(currency)),
            'amount': int(total_amount*1000),
            'pageView':"DESKTOP",
            "failUrl": merchant_detail.clictopay_url().get('failUrl'),
            # 'sessionTimeoutSecs':30,
            }
        url = merchant_detail.clictopay_url().get('pay_page_url')+"?"+urlencode(clictopay_tx_values)
        result = requests.post(url= url)
        request_params = literal_eval(result.text)
        _logger.info("-----request_params-%r-",request_params)
        return request_params


    @http.route([_return_url], type='http', auth='public', website=True)
    def clictopay_feedback(self, **post):
        merchant_detail = request.env["payment.acquirer"].sudo().search([("provider","=","clictopay")])
        try:
            params = {
                'userName': merchant_detail.detail_clictopay_payment_acquire().get('Username'),
                'password': merchant_detail.detail_clictopay_payment_acquire().get('Password'),
                'orderId': post.get('orderId')
                }
            url = str(merchant_detail.clictopay_url().get("order_status"))+"?"+ urlencode(params)
            result = requests.get(url=url)
            request_params = json.loads(result.text)

        except Exception as e:
            request_params = {
            'status':'cancel',
            "reference_no": request.session.get('so_id'),
            'result': 'The payment is cancelled successfully!',
            'response_code': '403'
            }
            request.session.pop('so_id', None)
        request.env['payment.transaction'].form_feedback(request_params, 'clictopay')
        return werkzeug.utils.redirect('/payment/process')


    @http.route(["/payment/clictopay/failed"], type='http', auth='public', website=True)
    def clictopay_failed(self, **post):

        _logger.info("-------------failed-------post %r---",post)
