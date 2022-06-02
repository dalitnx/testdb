# -*- coding: utf-8 -*-
#################################################################################
# Author      : Cubicle technolabs
# Copyright(c): Cubicle technolabs
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
{
    # App information
    'name': 'POS Advance Search',
    'version': '12.0.0',
    'summary': '',
    'category': 'Point Of Sale',
    'license': 'OPL-1',
    'images': ['static/description/cover_image.png'],

    # Dependencies
    'depends': ['base', 'point_of_sale'],

    # views
    'data': [
        'views/pos_advance_search_assets.xml',
    ],

    'qweb': [],

    # Author
    'author': 'Cubicle Technolabs',
    'website': 'https://cubicle-technolabs.odoo.com',
    'maintainer': 'Cubicle Technolabs',

    'installable': True,
    'application': True,
    'auto_install': False,
}
