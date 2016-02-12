# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    label_printer_id = fields.Many2one(string='Label Printer', comodel_name='mrp.label_printer')
