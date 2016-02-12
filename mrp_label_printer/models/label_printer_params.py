# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import fields, models


class LabelPrinterParams(models.Model):
    _name = 'mrp.label_printer.params'

    name = fields.Char(required=True)
    value = fields.Char()
    label_printer_id = fields.Many2one('mrp.label_printer', ondelete='cascade')
