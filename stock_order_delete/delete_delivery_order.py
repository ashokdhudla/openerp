from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import netsvc
from openerp import tools
from openerp.tools import float_compare, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp

class deletion_of_delivery_orders(osv.osv):
    
    _inherit = "stock.picking"
    
    def unlink(self, cr, uid,ids, context=None):
        move_obj = self.pool.get('stock.move')
        if context is None:
            context = {}
        for pick in self.browse(cr, uid, ids, context=context):
            if pick.state in ['done']:
                print pick.state
                raise osv.except_osv(_('Error!'), _('You cannot remove the picking which is in %s state!')%(pick.state,))
            else:
                ids2 = [move.id for move in pick.move_lines]
                ctx = context.copy()
                ctx.update({'call_unlink':True})
                if pick.state != 'draft':
                    #Cancelling the move in order to affect Virtual stock of product
                    move_obj.action_cancel(cr, uid, ids2, ctx)
                #Removing the move
                move_obj.unlink(cr, uid, ids2, ctx)

        return super(deletion_of_delivery_orders, self).unlink(cr, uid, ids, context=context)
deletion_of_delivery_orders()

class stock_pick_delete(osv.osv):
     _inherit = "stock.picking.out"
     
     def _workflow_trigger(self, cr, uid, ids, trigger, context=None):
        #override in order to trigger the workflow of stock.picking at the end of create, write and unlink operation
        #instead of it's own workflow (which is not existing)
        return self.pool.get('stock.picking')._workflow_trigger(cr, uid, ids, trigger, context=context)
    
stock_pick_delete()
     
     
     
     