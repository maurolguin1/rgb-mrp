# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import fields, models


class LabelProtocol(models.Model):
    _name = 'mrp.label_protocol'

    name = fields.Char(required=True)
