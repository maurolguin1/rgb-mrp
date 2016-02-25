RGB MRP Label Printer
=====================

This module adds support for label printers in the Manufacturing area.

Installation
------------

This module is designed to be installed on the *main Odoo server*.
On the *PosBox*, you should install the module *hw_serial*.

Configuration
-------------

This module supports the following thermal label printers: *ZEBRA*, *SATO*, *ARGOX*.
The printers can be configured on the main Odoo server, in the menu *Manufacturing >
Configuration > Label Printer*.

In the printer configuration, the following parameters can be defined:

- *Protocol*: PPLA / PPLB
- *Proxy url*: the PosBox url (http://IP:PORT) 
- *Serial port parameters*: baudrate, bytesize, stopbits, parity, timeout, serial port

The labes are created as templates, allowing to define dynamical fields, similar to the
Odoo email templates: *${object.field}*

Usage
-----

In the *manufacturing orders* form view, a new button is added, *Print Labels*, that allows
to print labels for the manufactured product.

Labels can also be printed for *serial numbers*, pushing the button *Print Labels*, in the
serial numbers form view.

Credits
=======

License
-------

* [GNU Affero General Public License] (http://www.gnu.org/licenses/agpl.html)

Author
------

* Copyright, RGB Consulting SL (www.rgbconsulting.com)

Contributors
------------

* RGB Consulting SL <odoo@rgbconsulting.com>
