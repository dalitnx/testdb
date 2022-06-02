# -*- coding: utf-8 -*-
#################################################################################
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    You should have received a copy of the License along with this program.
#    If not, see <https://store.webkul.com/license.html/>
#################################################################################

import logging
import requests
import json
import base64
import math

from datetime import datetime
from odoo import fields, models, api
from odoo.exceptions import UserError, Warning, ValidationError

_logger = logging.getLogger(__name__)


class TarguiData():

    APIEND = {
        "test": {
            'token': 'http://195.154.36.149:88/WebServiceExterne/get_token',
            'shipment': 'http://195.154.36.149:88/WebServiceExterne/pos_create',
            'label': 'http://195.154.36.149:88/WebServiceExterne/get_label',
        },
        "production": {
            'token': 'https://administrateur.targuiexpress.com/WebServiceExterne/get_token',
            'shipment': 'https://administrateur.targuiexpress.com/WebServiceExterne/pos_create',
            'label': 'https://administrateur.targuiexpress.com/WebServiceExterne/get_label',
        },
    }

    def __init__(self, *args, **kwargs):
        self.targui_test_username = kwargs.get('targui_test_username')
        self.targui_test_password = kwargs.get('targui_test_password')
        self.targui_prod_username = kwargs.get('targui_prod_username')
        self.targui_prod_password = kwargs.get('targui_prod_password')
        self.targui_mr_code = kwargs.get('targui_mr_code')
        self.targui_enviroment = kwargs.get('targui_enviroment')
        self.targui_fixed_rate = kwargs.get('targui_fixed_rate')

    def request_headers(self):
        targui_header = dict()
        targui_header['Content-Type'] = 'application/json'
        return targui_header

    def check_error(self, resp):
        resp_data = dict()
        if int(resp.status_code) in range(200, 300):
            resp_data['data'] = resp
            resp_data['error'] = False
        else:
            resp_data['error'] = True
        return resp_data

    def send_request(self, url=None, data=None):
        try:
            request_header = self.request_headers()
            _logger.info("==========REQ DATA=============%s", data)
            response = requests.post(
                url=url, data=json.dumps(data), headers=request_header)
            _logger.info("==========RESP DATA=============%s", response.text)
            checked_data = self.check_error(response)
            return checked_data
        except Exception as e:
            _logger.warning(
                "#WKDEBUG---TARGUI Exception-----%r---------" % (e))
            return dict(error=True, message=e)

    def get_targui_token(self):
        data = {}
        url = None
        if self.targui_enviroment == "test":
            data['USERNAME'] = self.targui_test_username
            data['PASSWORD'] = self.targui_test_password
            url = self.APIEND.get(self.targui_enviroment).get('token')
        else:
            data['USERNAME'] = self.targui_prod_username
            data['PASSWORD'] = self.targui_prod_password
            url = self.APIEND.get(self.targui_enviroment).get('token')

        resp = self.send_request(url=url, data=data)
        if resp.get('error'):
            raise UserError("WK:- Targui Error")
        return resp.get('data').text[1:-1]

    def get_targui_address_data(self, data):
        add_data = ""
        if data.get('street'):
            add_data = add_data + data.get('street') + ", "
        if data.get('street2'):
            add_data = add_data + data.get('street2') + ", "
        if data.get('city'):
            add_data = add_data + data.get('city') + ", "
        if data.get('state_name'):
            add_data = add_data + data.get('state_name') + ", "
        if data.get('country_name'):
            add_data = add_data + data.get('country_name') + ", "
        return add_data

    def get_order_auto_weight(self, order=None):
        total_wt = 0.0
        for ol in order.order_line:
            total_wt = total_wt + ol.product_uom_qty*ol.product_id.weight
        return round(total_wt, 2)

    def get_targui_order_weight(self, order=None):
        total_weight = 0.0
        if order.create_package == "auto":
            ep_packaging = order.carrier_id.packaging_id
            total_weight = self.get_order_auto_weight(order=order)
        if order.create_package == 'manual':
            ep_packaging = order.wk_packaging_ids and order.wk_packaging_ids[0]
            total_weight = round(ep_packaging.weight, 2)
        return total_weight

    def get_targui_rate(self, order=None):
        rate = 0.0
        total_shipment_weight = self.get_targui_order_weight(order=order)
        if total_shipment_weight <= 10.00:
            rate = self.targui_fixed_rate
        elif total_shipment_weight > 10.00 and total_shipment_weight <= 30:
            rate = self.targui_fixed_rate + \
                math.ceil(total_shipment_weight - 10)*0.5
        elif total_shipment_weight > 30.00:
            rate = 50
        return round(rate, 2)

    def generate_targui_shipment_data(self, pickings=None):
        data = {}
        shipper_info = pickings.carrier_id.get_shipment_shipper_address(
            picking=pickings)
        recipient_info = pickings.carrier_id.get_shipment_recipient_address(
            picking=pickings)

        data['TOKEN'] = self.get_targui_token()
        data['ENL_CONTACT_NOM'] = shipper_info.get('name')
        if shipper_info.get('name'):
            data['ENL_CONTACT_PRENOM'] = shipper_info.get('name')
        data['ENL_ADRESSE'] = self.get_targui_address_data(shipper_info)
        if shipper_info.get('phone'):
            data['ENL_PORTABLE'] = shipper_info.get('phone')
        if shipper_info.get('email'):
            data['ENL_MAIL'] = shipper_info.get('email')
        data['ENL_CODE_POSTAL'] = shipper_info.get('zip')

        data['LIV_CONTACT_NOM'] = recipient_info.get('name')
        if recipient_info.get('name'):
            data['LIV_CONTACT_PRENOM'] = recipient_info.get('name')
        data['LIV_ADRESSE'] = self.get_targui_address_data(recipient_info)
        if recipient_info.get('phone'):
            data['LIV_PORTABLE'] = recipient_info.get('phone')
        if recipient_info.get('email'):
            data['LIV_MAIL'] = recipient_info.get('email')
        data['LIV_CODE_POSTAL'] = recipient_info.get('zip')

        data['POIDS'] = pickings.shipping_weight
        data['VALEUR'] = pickings.sale_id.amount_total
        data['COD'] = pickings.sale_id.amount_total
        data['RTRNCONTENU'] = None
        data['DATE_ENLEVEMENT'] = pickings.scheduled_date.strftime("%d/%m/%Y")
        data['REFERENCE'] = pickings.name
        data['ORDER_NUMBER'] = pickings.sale_id.name
        data['MR_CODE'] = self.targui_mr_code
        data['DATE_LIVRAISON'] = pickings.scheduled_date.strftime("%d/%m/%Y")
        return data

    def generate_shipping_label(self, shipment_number):
        data = {}
        data['TOKEN'] = self.get_targui_token()
        data['POSBARCODE'] = shipment_number
        url = None
        if self.targui_enviroment == "test":
            url = self.APIEND.get(self.targui_enviroment).get('label')
        else:
            url = self.APIEND.get(self.targui_enviroment).get('label')

        resp = self.send_request(url=url, data=data)
        if resp.get('error'):
            raise UserError("WK:- Targui Error")
        return resp.get('data')

    def get_shipment_attachements(self, shipment):
        attchments = []
        shipping_documents = self.generate_shipping_label(shipment)
        att_data = ('TARGUI-' + str(shipment) +
                    '.pdf', shipping_documents.content)
        attchments.append(att_data)
        return attchments

    def get_targui_shipment(self, pickings=None):
        shipment_data = self.generate_targui_shipment_data(pickings=pickings)
        url = None
        if self.targui_enviroment == "test":
            url = self.APIEND.get(self.targui_enviroment).get('shipment')
        else:
            url = self.APIEND.get(self.targui_enviroment).get('shipment')

        resp_data = self.send_request(url=url, data=shipment_data)
        if resp_data.get('error'):
            raise UserError("WK:- Targui Error")

        data = resp_data.get('data').text
        try:
            data = data[1:-1]
        except Exception as e:
            _logger.warning("WK- TARGUI WARNING-----%s", e)
            raise UserError(data)
        return data


class TarguiDeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    @api.model
    def targui_rate_shipment(self, order):
        currency_id = self.get_shipment_currency_id(order)
        currency_code = currency_id.name
        if self.prod_environment:
            config = self.wk_get_carrier_settings(['targui_prod_username', 'targui_prod_password'])
            config['targui_enviroment'] = 'production'
        else:
            config = self.wk_get_carrier_settings(['targui_test_username', 'targui_test_password'])
            config['targui_enviroment'] = 'test'
        config['targui_currency'] = currency_code
        config['targui_fixed_rate'] = self.targui_fixed_rate
        sdk = TarguiData(**config)

        targui_rate = sdk.get_targui_rate(order=order)

        return {
            'success': True,
            'price': targui_rate,
            'error_message': False,
            'warning_message': False,
        }
        
    @api.model
    def targui_send_shipping(self, pickings):
        result = {
            'exact_price': 0,
            'weight': 0,
            'date_delivery': None,
            'tracking_number': '',
            'attachments': []
        }
        currency_id = self.get_shipment_currency_id(pickings=pickings)
        currency_code = currency_id.name
        if self.prod_environment:
            config = self.wk_get_carrier_settings(['targui_prod_username', 'targui_prod_password'])
            config['targui_enviroment'] = 'production'
        else:
            config = self.wk_get_carrier_settings(['targui_test_username', 'targui_test_password'])
            config['targui_enviroment'] = 'test'
        config['targui_fixed_rate'] = self.targui_fixed_rate
        config['targui_mr_code'] = self.targui_mr_code
        sdk = TarguiData(**config)
        _logger.info(" -- - -- Check check check - -- ")
        targui_shipment = sdk.get_targui_shipment(pickings=pickings)
        result['tracking_number'] = str(targui_shipment)
        result['attachments'] = sdk.get_shipment_attachements(targui_shipment)
        return result

    @api.model
    def targui_cancel_shipment(self, pickings):
        raise UserError("Targui don't support shipment cancellation")

    @api.model
    def targui_get_tracking_link(self, pickings):
        for obj in self:
            targui_tracking_url = "https://targuiexpress.com/"
            return targui_tracking_url
