# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import fields, models, api

CONTROL_CODES = {'<SOH>': 1, '<STX>': 2, '<ACK>': 6, '<LF>': 10, '<CR>': 13, '<XON>': 17, '<XOFF>': 19, '<NAK>': 21, '<ESC>': 27}


class LabelTemplate(models.Model):
    _name = 'mrp.label_template'

    name = fields.Char(required=True)
    protocol_id = fields.Many2one(string='Protocol', comodel_name='mrp.label_protocol')
    product_quantity = fields.Integer(help='The quantity of product for each label', default=1)
    template_code = fields.Text(string='Template')
    product_id = fields.Many2one(string='Product', comodel_name='product.product')
    category_id = fields.Many2one(string='Product Category', comodel_name='product.category')
    type = fields.Selection([('mrp.production', 'Manufacturing Orders'), ('stock.production.lot', 'Serial Numbers')])

    @api.multi
    def render_template(self, params, model, rec_id):
        # Render label template
        template = self.env['email.template'].render_template_batch(self.template_code, model, [rec_id])
        template = template.get(rec_id, '')
        # Translate params
        for param, value in params.iteritems():
            template = template.replace(param, value)
        # Clear line breaks
        template = template.replace('\r', '').replace('\n', '')
        # Convert control codes
        for code, value in CONTROL_CODES.iteritems():
            template = template.replace(code, chr(value))
        # Encode unsupported unicode data
        template = template.encode('ascii', 'ignore')
        return template
