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

{
    'name':           "Targui Delivery Carrier",
    'summary':           """
                                    Targui  Delivery Carrier
                                """,
    'description':           """
                                    Targui Delivery Carrier
                                """,
    'author':           "Webkul Software Pvt. Ltd.",
    'website':           "https://store.webkul.com",
    'category':           'Website',
    'license':           'Other proprietary',
    'maintainer':           'Pragyat Singh Rana',
    'version':           '1.0.0',
    'depends':           [
        'odoo_shipping_service_apps',
    ],

    'data':           [
        'security/ir.model.access.csv',
        'views/targui_shipping_service.xml',
        'data/data.xml',
    ],
    'images':           ['static/description/Banner.gif'],
    'application':           True,
    'installable':           True,
    'price':           199,
    'currency':           'USD',
    'per_init_hook':           'pre_init_check',
}
