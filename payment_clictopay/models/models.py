# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

import re
import logging

import dateutil.parser

from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
import pprint
from odoo.fields import Datetime
from odoo.http import request
_logger = logging.getLogger(__name__)


class AcquirerClickToPay(models.Model):

    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('clictopay', 'ClickToPay')], ondelete={'clictopay': 'set default'})

    clictopay_username = fields.Char('Username', required_if_provider='ClickToPay', groups='base.group_user', help='Merchant Login received during registration.')
    clictopay_password = fields.Char('Password', groups='base.group_user',help='merchant password received upon registration. ')


    def clictopay_url(self):
        base_url = request.httprequest.host_url
        return{
        "pay_page_url" : "https://test.clictopay.com/payment/rest/register.do",
        'order_status':'https://test.clictopay.com/payment/rest/getOrderStatus.do',
        'return_url': base_url+'clictopay/feedback',
        'failUrl': base_url+"payment/clictopay/failed",
        }

    def detail_clictopay_payment_acquire(self):
        return{
        "Username":self.clictopay_username,
        "Password":self.clictopay_password,
        # "paytabs_site_url":self.clictopay_password
        }

class TransactionClicToPay(models.Model):
    _inherit = 'payment.transaction'

    clictopay_txn_id = fields.Char('Transaction ID')

    @api.model
    def _clictopay_form_get_tx_from_data(self,  data):
        reference = data.get('OrderNumber')
        tx = self.env['payment.transaction'].sudo().search([('reference', '=', reference)])
        if not tx:
            error_msg = _('ClickToPay: received data with missing reference (%s)') % (reference)
            raise ValidationError(error_msg)
        return tx

    
    def _clictopay_form_validate(self, data):
        res = {}
        if data.get('OrderStatus') == 2:
            res = {
                'date':fields.datetime.now(),
                'acquirer_reference': data.get('transaction_id'),
                'clictopay_txn_id': data.get('transaction_id'),
                }
            self.write(res)
            return self._set_transaction_done()
        else:
            if data.get("status") == "cancel":
                res.update({
                'date':fields.datetime.now(),
                })
                self.write(res)
                return self._set_transaction_cancel()
            else:
                res.update({
                'clictopay_txn_id': data.get('transaction_id'),
                'acquirer_reference': data.get('transaction_id'),
                'date':fields.datetime.now(),

                })
                self.write(res)
                return self._set_transaction_error(data.get('ErrorMessage'))
