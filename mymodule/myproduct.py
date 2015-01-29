from openerp.osv import fields, osv

class product_extend(osv.osv):
  _name="product.product"
  _inherit="product.product"
  _columns = {
    'purchase_price': fields.float('Purchase Price'),
  }

product_extend()
