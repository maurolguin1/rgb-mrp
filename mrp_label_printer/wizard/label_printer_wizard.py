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
    label_printer = fields.Many2one(comodel_name='mrp.label_printer')
    label_template = fields.Many2one(comodel_name='mrp.label_template')
    number_of_labels = fields.Integer('No. labels')

    @api.onchange('manufacture_order')
    def _set_default(self):
        # Assign wizard default values
        self.product = self.manufacture_order.product_id
        self.product_quantity = self.manufacture_order.product_qty
        self.manufacture_date = self.manufacture_order.date_planned
        self.label_printer = self.env.user.label_printer_id
        # Add domain to label_templates
        labels = [l.id for l in self.env['mrp.label_template'].search(
            ['&', ('protocol_id.id', '=', self.label_printer.protocol_id.id),
             '|', '&', ('product_id', '=', False), ('category_id', '=', False),
             '|', ('product_id.id', '=', self.product.id), ('category_id.id', '=', self.product.categ_id.id)])]
        return {'domain': {'label_template':[('id', 'in', labels)]}}

    @api.onchange('label_template')
    def _number_of_labels(self):
        if self.label_template:
            self.number_of_labels = ceil(self.product_quantity / self.label_template.product_quantity)

    @api.multi
    def print_labels(self):
        params = {}
        template_var = {}
        # Add printer params
        for param in self.label_printer.params_ids:
            params[param.name] = param.value
        params['proxy_url'] = self.label_printer.proxy_url
        template_var['$[number_of_labels]'] = format(self.number_of_labels - 1, '04')
        params['data'] = self._render_template(template_var)
        # Return client action
        result = {
            "type": "ir.actions.client",
            "tag": "label_printer",
            "params": params
        }
        return result

    @api.multi
    def _render_template(self, params):
        # Render label template
        template = self.env['email.template'].render_template_batch(self.label_template.template_code,
                                                                    'mrp.production',[self.manufacture_order.id])
        template = template.get(self.manufacture_order.id, '')
        for param, value in params.iteritems():
            template = template.replace(param, value)
        return template
