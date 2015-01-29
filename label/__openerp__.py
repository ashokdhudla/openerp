# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today Serpent Consulting Services (<http://www.serpentcs.com>)
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name" : "Mass Reporting",
    "version" : "1.1",
    "author" : "Serpent Consulting Services Pvt. Ltd.",
    "category" : "Tools",
    "website" : "http://www.serpentcs.com",
    "description": """
    This is the module for generic label printing with multiple size configuration with barcode, image and description.
    The video of 6.1 compatible module is here: https://www.youtube.com/watch?v=VV6k5rDWEUo
    The video of v7 module to arrive soon.
    
    Packages to pre-install:
    Barcode : https://pypi.python.org/pypi/pyBarcode/0.7
    RSVG : sudo apt-get install python-rsvg
    Cairo : https://pypi.python.org/pypi/CairoSVG/1.0.6
    """,
    'depends': ['report_webkit'],
    'init_xml': [],
    'update_xml': [
        'security/label.brand.csv',
        'security/label.config.csv',
        'wizard/label_print_wizard_view.xml',
        'label_print_view.xml',
        'label_config_view.xml',
        'label_size_data.xml',
        'label_report.xml',
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
