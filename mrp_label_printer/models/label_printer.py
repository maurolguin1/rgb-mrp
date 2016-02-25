# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import fields, models, api


class LabelPrinter(models.Model):
    _name = 'mrp.label_printer'

    name = fields.Char(required=True)
    location = fields.Char()
    protocol_id = fields.Many2one(string='Protocol', comodel_name='mrp.label_protocol')
    proxy_url = fields.Char(size=45, help='This field is used to define the proxy url - HTTP://IP:PORT')
    params_ids = fields.One2many('mrp.label_printer.params', 'label_printer_id')

    @api.multi
    def get_params(self):
        params = {}
        params['proxy_url'] = self.proxy_url
        for param in self.params_ids:
            params[param.name] = param.value
        return params
