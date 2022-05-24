# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class zenhost(models.Model):
#     _name = 'zenhost.zenhost'
#     _description = 'zenhost.zenhost'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100




class wamiadev(models.Model):
    _name='zenhost.zenhost'
    t1 = fields.Char("Empoloyee name")
    t2=fields.Datetime("Recrutement Date")
    t3=fields.Many2one("res.users","Empoloyee name")
    t4=fields.Text("supervisor Notes")
    largemeal = fields.Boolean("Large Meal")