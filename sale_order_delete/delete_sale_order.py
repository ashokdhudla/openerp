from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools import amount_to_text_en
import re
from openerp.tools.translate import _

class sale_order_delete(osv.osv):
    _inherit="sale.order"
    
    def unlink(self, cr, uid, ids, context=None):
        sale_orders = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for s in sale_orders:
            if s['state'] in ['draft', 'cancel','done']:
                unlink_ids.append(s['id'])
            else:
                raise osv.except_osv(_('Invalid Action!'), _('In order to delete a confirmed sales order, you must cancel it.\nTo do so, you must first cancel related picking for delivery orders.'))

        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)
    
sale_order_delete()