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

from osv import fields, osv
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import evernote
from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
from evernote.edam.notestore import NoteStore
import xml.etree.ElementTree as etree
import time
import re
from datetime import datetime
from  create_evernote_atta import EvernoteUpload


class openerp_evernote(osv.osv):
    
    _name = 'openerp.evernote'
    
    _columns = {
                'name' : fields.char("Evernote", size = 100),
                'evernote_id' : fields.many2one("product.product"),
                'url' : fields.char("URL", size=100),
                'description' : fields.text('Description'),
                'date' : fields.date("Date")
                }   
    
    def onchange_url(self, cr, uid, ids, url, evernote_id,context=None):
        if context is None:
            context={}
        
        if not url:
            raise osv.except_osv(('Warning!'), ('Please enter  url !'))
        if url[0:16] != 'evernote:///view':
            raise osv.except_osv(('Warning!'), ('Please check url !'))
            
        guid = re.findall('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',url)
    
        if not guid:
            raise osv.except_osv(('Warning!'), ('Please check url !'))
      
        auth_token = "S=s1:U=72d01:E=1479a33c4dd:C=140428298df:P=1cd:A=en-devtoken:V=2:H=f85f82d8927640558388d21d02819d7f"
        try:
            client = EvernoteClient(token=auth_token, sandbox=False)
        except : 
            raise osv.except_osv(('Warning!'), ('Please check token information!'))
        
                
        note = client.get_note_store().getNote(guid[0],True,True,True,True)
        noteStore = client.get_note_store()
        getnote = noteStore.getNote(guid[0],True,True, True, True)
        note_created = getnote.created
        note_date = time.strftime('%Y-%m-%d',  time.gmtime(note_created/1000))
        xml = etree.fromstring(getnote.content)
        content = xml.text
        title = note.title
                
        return {'value' : {'name' : title,'description': content ,'date' : note_date}}

openerp_evernote()


class product_product(osv.osv):

    _inherit = 'product.product'
    
    _columns = {
                'evernote_ids' : fields.one2many("openerp.evernote", "evernote_id","Evernote"),
                }
    
product_product()

class purchase_order(osv.osv):
   
    _inherit = 'purchase.order'
    
    _columns = {
                'evernote_ids' : fields.one2many("openerp.evernote", "evernote_id","Evernote"),
                }
    
purchase_order()

class res_partner(osv.osv):
    
    _inherit = 'res.partner'
    
    _columns = {
                'evernote_ids' : fields.one2many("openerp.evernote", "evernote_id","Evernote"),
                }
    
   
res_partner()

class bank_statement(osv.osv):
  
    _inherit = 'account.bank.statement'
    
    _columns = {
                'evernote_ids' : fields.one2many("openerp.evernote", "evernote_id","Evernote"),
                }
    
   
bank_statement()

class hr_timesheet_sheet(osv.osv):
   
    _inherit = 'hr_timesheet_sheet.sheet'
                
    _columns = {
                'evernote_ids' : fields.one2many("openerp.evernote", "evernote_id","Evernote"),
                }
    
   
hr_timesheet_sheet()

class hr_expenses_expenses(osv.osv):
   
    _inherit = 'hr.expense.expense'
    
    _columns = {
                'evernote_ids' : fields.one2many("openerp.evernote", "evernote_id","Evernote"),
                }
   
hr_expenses_expenses()

class stock_picking_in(osv.osv):
    
    _inherit = 'stock.picking.in'
    _columns = {
                'evernote_ids' : fields.one2many("openerp.evernote", "evernote_id","Evernote"),
                }
    
   
stock_picking_in()


class project_project(osv.osv):
   
    _inherit = 'project.project'
    
    _columns = {
                'evernote_ids' : fields.one2many("openerp.evernote", "evernote_id","Evernote"),
                }
project_project()

class account_bank_statement_line(osv.osv):
    
    _inherit = 'account.bank.statement.line'
    
    _columns = {
                'evernote_ids' : fields.one2many("openerp.evernote", "evernote_id","Evernote"),
                }
   
account_bank_statement_line()

class project_task(osv.osv):

    _inherit = 'project.task'
    
    _columns = {
                'note_created' : fields.boolean("Created Note" ,readonly=1),
    }
   
    def create_note(self, cr, uid, ids, context = None):
        
        auth_token = "S=s1:U=72d01:E=1479a33c4dd:C=140428298df:P=1cd:A=en-devtoken:V=2:H=f85f82d8927640558388d21d02819d7f"
        try:
            client = EvernoteClient(token=auth_token, sandbox=False)
        except : 
            raise osv.except_osv(('Warning!'), ('Please check token information!'))
         
        c1 = EvernoteUpload(auth_token)
        c1.upload_to_notebook('report1.pdf', 'boom')
        note_data = self.browse(cr, uid, ids[0], context=context)
        if not note_data.note_created:
            try:
                note_store = client.get_note_store()
                notebooks = note_store.listNotebooks()
                note = Types.Note()
                note.title = str(note_data.name)
                note_cont = str(note_data.description)
                note.content = '<?xml version="1.0" encoding="UTF-8"?>'
                note.content += '<!DOCTYPE en-note SYSTEM ' \
                    '"http://xml.evernote.com/pub/enml2.dtd">'
                note.content += '<en-note>'
                note.content += str(note_cont)
                note.content += '</en-note>'

                created_note = note_store.createNote(note)
                self.write(cr, uid, ids[0], {'note_created':1}, context=context)
            except:
                raise osv.except_osv(('Warning !'), ('Please check internet connection.!'))
        else:
            raise osv.except_osv(('Error!'), ('Already Created.!'))
        return True
    
    
    def wizard_call(self,cr,uid,ids,context=None):
        self_data = self.browse(cr, uid, ids, context=context)
        if not self_data[0].note_created:
            return {
                'view_type':'form',
                'view_mode':'form',
                'res_model':'create.note.wizard',
                'target' : 'new',
                'type':'ir.actions.act_window',
                'context':context,
            }
        else:
            raise osv.except_osv(('Warning!'), ('Already Created.!'))
            
project_task()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
