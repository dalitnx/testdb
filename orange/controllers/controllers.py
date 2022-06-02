# -*- coding: utf-8 -*-
# from odoo import http


# class Orange(http.Controller):
#     @http.route('/orange/orange', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/orange/orange/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('orange.listing', {
#             'root': '/orange/orange',
#             'objects': http.request.env['orange.orange'].search([]),
#         })

#     @http.route('/orange/orange/objects/<model("orange.orange"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('orange.object', {
#             'object': obj
#         })
