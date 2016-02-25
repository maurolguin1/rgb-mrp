# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import fields, models, api


class LabelTemplate(models.Model):
    _name = 'mrp.label_template'

    name = fields.Char(required=True)
    protocol_id = fields.Many2one(string='Protocol', comodel_name='mrp.label_protocol')
    product_quantity = fields.Integer(help='The quantity of product for each label', default=1)
    template_code = fields.Text(string='Template')
    product_id = fields.Many2one(string='Product', comodel_name='product.product')
    category_id = fields.Many2one(string='Product Category', comodel_name='product.category')
    type = fields.Selection([('mrp.production', 'Manufacturing Orders'),
                             ('stock.production.lot', 'Serial Numbers')])

    @api.multi
    def render_template(self, params, model, rec_id):
        # Render label template
        template = self.env['email.template'].render_template_batch(self.template_code, model,
                                                                    [rec_id])
        template = template.get(rec_id, '')
        for param, value in params.iteritems():
            template = template.replace(param, value)
        return template
