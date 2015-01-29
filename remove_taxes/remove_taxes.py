from openerp.osv import osv, fields

class remove_taxes_purchase(osv.osv):

	_inherit = 'purchase.order'

	_columns = {

	}

remove_taxes_purchase()

class remove_taxes_sales(osv.osv):

	_inherit = 'sale.order'
	_columns = {

	}
remove_taxes_sales()

class hide_productline_stock(osv.osv):

	_inherit = 'stock.picking.out'

	_columns = {

	}
hide_productline_stock()

class stock_picking(osv.osv):

	_inherit='stock.picking'

	_columns = {

	}
stock_picking()

