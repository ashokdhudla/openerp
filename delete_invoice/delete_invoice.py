from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import netsvc
from openerp import tools
from openerp.tools import float_compare, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
class deletion_of_cancel_invoice(osv.osv):
    _inherit = "account.invoice"
    
    def unlink(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        invoices = self.read(cr, uid, ids, ['state','internal_number'], context=context)
        unlink_ids = []

        for t in invoices:
            if t['state'] not in ('draft', 'cancel'):
                raise openerp.exceptions.Warning(_('You cannot delete an invoice which is not draft or cancelled. You should refund it instead.'))
            #===================================================================
            # elif t['internal_number']:
            #     raise openerp.exceptions.Warning(_('You cannot delete an invoice after it has been validated (and received a number).  You can set it back to "Draft" state and modify its content, then re-confirm it.'))
            #===================================================================
            else:
                unlink_ids.append(t['id'])

        osv.osv.unlink(self, cr, uid, unlink_ids, context=context)
        return True
    
deletion_of_cancel_invoice()