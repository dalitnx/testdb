# -*- coding: utf-8 -*-
# from odoo import http


# class Zenhost(http.Controller):
#     @http.route('/zenhost/zenhost', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/zenhost/zenhost/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('zenhost.listing', {
#             'root': '/zenhost/zenhost',
#             'objects': http.request.env['zenhost.zenhost'].search([]),
#         })

#     @http.route('/zenhost/zenhost/objects/<model("zenhost.zenhost"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('zenhost.object', {
#             'object': obj
#         })
