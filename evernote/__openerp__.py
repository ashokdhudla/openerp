# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2011 Serpent Consulting Services (<http://serpentcs.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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
    "name": "OpenERP-Evernote",
    "version": "1.0",
    "depends": [
        "crm",
        "product",
        "purchase",
        "hr",
        "account",
        "project",
        "stock" 
    ],
    "author": "Serpent Consulting Services Pvt. Ltd.",
    'website': 'http://www.serpentcs.com',
    "description": """
        This module made integration between OpenERP and Evernote.
    """,
    'data': [
        'configuration_view.xml',
        'openerp_evernote_view.xml',
        'wizard/project_task_create_note_view.xml',
        'crm_phon_call_view.xml'
    ],
    'installable': True,
    'auto_install':False,
    'application':True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: