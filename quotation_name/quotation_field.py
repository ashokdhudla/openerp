from openerp.osv import fields, osv
class new_quotation_name(osv.osv):
    _inherit="sale.order"
    _columns={
        'quotation_name':fields.char('Quotation Name', size=60),
    
        }

new_quotation_name()