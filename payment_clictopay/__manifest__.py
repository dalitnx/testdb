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
  "name"                 :  "ClicToPay Payment Acquirer",
  "summary"              :  """The module allow the customers to make payments on Odoo website using ClicToPay Payment Gateway. The module facilitates ClicToPay integration with Odoo""",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "depends"              : ['payment','website_sale'],
  "data"                 : [
                            # 'security/ir.model.access.csv',
                            'views/templates.xml',
                            'views/payment_views.xml',
                            'data/data.xml',
                        ],

}
