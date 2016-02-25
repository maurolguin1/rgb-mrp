# -*- coding: utf-8 -*-
##############################################################################
#
#   MRP Label Printer
#   Copyright 2016 RGB Consulting, SL
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "MRP Label Printer",
    'version': '1.0',
    'depends': ['mrp'],
    'license': 'AGPL-3',
    'author': "RGB Consulting SL",
    'website': "http://www.rgbconsulting.com",
    'category': 'Manufacturing',
    'summary': """Label printers for manufacturing orders""",
    'description': """
MRP Label Printer
=================
This module allows to print labels for manufactured products, with printers using the *PPLA* / *PPLB* protocol.\n
This module supports the following thermal label printers: *ZEBRA*, *SATO*, *ARGOX*\n
This module is designed to be installed on the *main Odoo server*. On the *PosBox*, you should install the module *hw_serial*.
    """,

    'data': [
        'security/ir.model.access.csv',
        'views/js.xml',
        'wizard/mrp_printer_wizard.xml',
        'wizard/lot_printer_wizard.xml',
        'views/label_printer.xml',
        'views/label_template.xml',
        'views/res_users.xml',
        'views/mrp_production.xml',
        'views/serial_number.xml',
    ],

    'demo': [
    ],
}
