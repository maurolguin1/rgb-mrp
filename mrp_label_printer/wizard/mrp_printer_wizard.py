# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import fields, models, api
from math import ceil


class LabelPrinterWizard(models.TransientModel):
    _name = 'mrp.label_printer.wizard'

    def _default_mo(self):
        return self.env['mrp.production'].browse(self._context.get('active_id'))

    manufacture_order = fields.Many2one(comodel_name='mrp.production', default=_default_mo, readonly=True)
    product = fields.Many2one(comodel_name='product.product', readonly=True)
    product_quantity = fields.Float(readonly=True)
    manufacture_date = fields.Datetime(readonly=True)
    label_printer = fields.Many2one(comodel_name='mrp.label_printer',
                                    default=lambda self: self.env.user.label_printer_id)
    label_template = fields.Many2one(comodel_name='mrp.label_template')
    number_of_labels = fields.Integer('No. labels')

    @api.onchange('label_printer')
    def _set_default(self):
        # Assign wizard default values
        self.product = self.manufacture_order.product_id
        self.product_quantity = self.manufacture_order.product_qty
        self.manufacture_date = self.manufacture_order.date_planned
        # Add domain to label_templates
        self.label_template = None
        labels = [l.id for l in self.env['mrp.label_template'].search(
            ['&', '|', ('type', '=', 'mrp.production'), ('type', '=', False),
             '&', ('protocol_id.id', '=', self.label_printer.protocol_id.id),
             '|', '&', ('product_id', '=', False), ('category_id', '=', False),
             '|', ('product_id.id', '=', self.product.id), ('category_id.id', '=', self.product.categ_id.id)])]
        return {'domain': {'label_template': [('id', 'in', labels)]}}

    @api.onchange('label_template')
    def _number_of_labels(self):
        if self.label_template:
            self.number_of_labels = ceil(self.product_quantity / self.label_template.product_quantity)

    @api.multi
    def print_labels(self):
        # Get printer params
        params = self.label_printer.get_params()
        # Render label template
        template_var = {}
        template_var['$[number_of_labels]'] = format(self.number_of_labels, '04')
        params['data'] = self.label_template.render_template(template_var, 'mrp.production', self.manufacture_order.id)
        # Return client action
        result = {
            "type": "ir.actions.client",
            "tag": "label_printer",
            "params": params
        }
        return result
