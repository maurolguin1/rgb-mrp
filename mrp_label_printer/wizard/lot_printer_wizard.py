# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import fields, models, api


class LotPrinterWizard(models.TransientModel):
    _name = 'mrp.label_printer.lot.wizard'

    def _default_sn(self):
        return self.env['stock.production.lot'].browse(self._context.get('active_id'))

    serial_number = fields.Many2one(comodel_name='stock.production.lot', default=_default_sn, readonly=True)
    product = fields.Many2one(comodel_name='product.product', readonly=True)
    label_printer = fields.Many2one(comodel_name='mrp.label_printer')
    label_template = fields.Many2one(comodel_name='mrp.label_template')
    number_of_labels = fields.Integer(string='No. labels', default=1)

    @api.onchange('serial_number')
    def _set_default(self):
        # Assign wizard default values
        self.product = self.serial_number.product_id
        self.label_printer = self.env.user.label_printer_id
        # Add domain to label_templates
        labels = [l.id for l in self.env['mrp.label_template'].search(
            ['&', '|', ('type', '=', 'stock.production.lot'), ('type', '=', False),
             '&', ('protocol_id.id', '=', self.label_printer.protocol_id.id),
             '|', '&', ('product_id', '=', False), ('category_id', '=', False),
             '|', ('product_id.id', '=', self.product.id), ('category_id.id', '=', self.product.categ_id.id)])]
        return {'domain': {'label_template': [('id', 'in', labels)]}}

    @api.multi
    def print_labels(self):
        # Get printer params
        params = self.label_printer.get_params()
        # Render label template
        template_var = {}
        template_var['$[number_of_labels]'] = format(self.number_of_labels - 1, '04')
        params['data'] = self.label_template.render_template(template_var, 'stock.production.lot',
                                                             self.serial_number.id)
        # Return client action
        result = {
            "type": "ir.actions.client",
            "tag": "label_printer",
            "params": params
        }
        return result
