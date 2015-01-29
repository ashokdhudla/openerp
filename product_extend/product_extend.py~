
from openerp.osv import fields, osv

class product_extend(osv.osv):
	_name ="product.product"
	_inherit="product.product"
	_columns ={
		'price_book_name':fields.char('Price Book Name',size=120),
		'reseller_sale_price':fields.float('Reseller Sale Price'),
		'cst_vat_tax':fields.many2one('account.tax','CST/VAT Tax'),
		'service_tax':fields.many2one('account.tax','Service Tax'),
	
	}	
product_extend()
