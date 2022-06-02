# -*- coding: utf-8 -*-
#################################################################################
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    You should have received a copy of the License along with this program.
#    If not, see <https://store.webkul.com/license.html/>
#################################################################################

import logging
from typing import DefaultDict

from odoo import fields, models, api
from odoo.exceptions import UserError, Warning, ValidationError

_logger = logging.getLogger(__name__)

MRCODES = [
    ('ESP', 'ESPECES'),
    ('CHQ', 'CHEQUE'),
    ('VIR', 'VIREMENT'),
    ('EFF', 'EFFET'),
    ('LC', 'LETTRE DE CREDIT'),
]


class TarguiDeliveryCarriers(models.Model):
    _inherit = 'delivery.carrier'

    delivery_type = fields.Selection(
        selection_add=[('targui', 'Targui')], ondelete={'targui': 'cascade'}
    )
    targui_test_username = fields.Char(
        string="Targui Test Username", default="dummyapi")
    targui_test_password = fields.Char(
        string="Targui Test Password", default="dummyapi")
    targui_prod_username = fields.Char(
        string="Targui Production Username", default="dummyapi")
    targui_prod_password = fields.Char(
        string="Targui Production Password", default="dummyapi")
    targui_mr_code = fields.Selection(
        selection=MRCODES, string="Targui MR Code", default="CHQ")
    targui_fixed_rate = fields.Float(string="Targui Fixed Rate", default=0.0)


class TarguiProductPackage(models.Model):
    _inherit = 'product.package'

    delivery_type = fields.Selection(
        selection_add=[('targui', 'Targui')], ondelete={'targui': 'cascade'}
    )


class TarguiProductPackaging(models.Model):
    _inherit = 'stock.package.type'

    package_carrier_type = fields.Selection(
        selection_add=[('targui', 'Targui')], ondelete={'targui': 'cascade'}
    )


class EasyshipStockPicking(models.Model):
    _inherit = 'stock.picking'

    easyship_tracking_url = fields.Char(string="Easyship Tracking URL")

    def get_all_wk_carriers(self):
        res = super(EasyshipStockPicking,self).get_all_wk_carriers()
        res.append('targui')
        return res
