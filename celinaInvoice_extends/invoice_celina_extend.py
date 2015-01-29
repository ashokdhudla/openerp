
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import openerp.addons.decimal_precision as dp
from openerp import netsvc
from openerp.tools import amount_to_text_en
import re

class sale_order_extend(osv.osv):
	_name ="sale.order"
	_inherit="sale.order"
	
	def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
		cur_obj = self.pool.get('res.currency')
		res = {}
		for order in self.browse(cr, uid, ids, context=context):
			res[order.id] = {
				'amount_untaxed': 0.0,
				'amount_tax': 0.0,
				'amount_total': 0.0,
				'amount_inwords':'',
			}
			val = val1 = 0.0
			cur = order.pricelist_id.currency_id
			for line in order.order_line:
				val1 += line.price_subtotal
				val += self._amount_line_tax(cr, uid, line, context=context)
			res[order.id]['amount_tax'] = cur_obj.round(cr, uid, cur, val)
			res[order.id]['amount_untaxed'] = cur_obj.round(cr, uid, cur, val1)
			res[order.id]['amount_total'] = res[order.id]['amount_untaxed'] + res[order.id]['amount_tax']
			# print cur.name
			amount_words = amount_to_text_en.amount_to_text(res[order.id]['amount_total'], 'en', cur.name)
			amount_words_new = re.match( r'(.*)AED(.*?) .*', amount_words, re.M|re.I),cur.name
			# res[order.id]['amount_inwords'] = amount_words_new[0].group(1)
		return res
		
	def _get_order(self, cr, uid, ids, context=None):
		result = {}
		for line in self.pool.get('sale.order.line').browse(cr, uid, ids, context=context):
			result[line.order_id.id] = True
		return result.keys()

		
	_columns ={
		'amount_inwords': fields.function(_amount_all, string='Amount in words',type='char',multi="sums",size=260),
		'validity_new': fields.char("Container No.",size=150),
		'warranty_new': fields.char("Seal No.",size=150),
		'availability_new': fields.char("Availability",size=150),
		'amount_untaxed': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total Amount',
			store={
				'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
				'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
			},
			multi='sums', help="The amount without tax.", track_visibility='always'),
		
	}

	def _prepare_invoice(self, cr, uid, order, lines, context=None):
		"""Prepare the dict of values to create the new invoice for a
		   sales order. This method may be overridden to implement custom
		   invoice generation (making sure to call super() to establish
		   a clean extension chain).

		   :param browse_record order: sale.order record to invoice
		   :param list(int) line: list of invoice line IDs that must be
								  attached to the invoice
		   :return: dict of value to create() the invoice
		"""
		# print lines
		if context is None:
			context = {}
		journal_ids = self.pool.get('account.journal').search(cr, uid,
			[('type', '=', 'sale'), ('company_id', '=', order.company_id.id)],
			limit=1)
		if not journal_ids:
			raise osv.except_osv(_('Error!'),
				_('Please define sales journal for this company: "%s" (id:%d).') % (order.company_id.name, order.company_id.id))
		line_id = self.pool.get('sale.order.line').search(cr,uid,[('order_id','=',order.id)])
		i = self.pool.get('sale.order.line').browse(cr,uid,line_id[0])
		lines_new = [{'uos_id': 1, 'product_id': i.product_id.id, 'unit_price': i.price_unit, 'account_id': 19, 'name': i.name, 'discount': 0, 't_weight': i.product_uom_qty, 'account_analytic_id': False, 'quantity': i.total_weight}]
		invoice_vals = {
			'name': order.client_order_ref or '',
			'origin': order.name,
			'type': 'out_invoice',
			'reference': order.client_order_ref or order.name,
			'account_id': order.partner_id.property_account_receivable.id,
			'partner_id': order.partner_invoice_id.id,
			'journal_id': journal_ids[0],
			'invoice_line': [(6, 0, lines)],
			'currency_id': order.pricelist_id.currency_id.id,
			'comment': order.note,
			'validity_new_invoice' : order.validity_new,
			'amount_inwords_invoice' : order.amount_inwords,
			'warranty_new_invoice' : order.warranty_new,
			'availability_new_invoice' :order.availability_new,
			'payment_term': order.payment_term and order.payment_term.id or False,
			'fiscal_position': order.fiscal_position.id or order.partner_id.property_account_position.id,
			'date_invoice': context.get('date_invoice', False),
			'company_id': order.company_id.id,
			'user_id': order.user_id and order.user_id.id or False
		}

		# Care for deprecated _inv_get() hook - FIXME: to be removed after 6.1
		invoice_vals.update(self._inv_get(cr, uid, order, context=context))
		return invoice_vals

	def _make_invoice(self, cr, uid, order, lines, context=None):
		print 'LINES',lines
		inv_obj = self.pool.get('account.invoice')
		obj_invoice_line = self.pool.get('account.invoice.line')
		if context is None:
			context = {}
		invoiced_sale_line_ids = self.pool.get('sale.order.line').search(cr, uid, [('order_id', '=', order.id), ('invoiced', '=', True)], context=context)
		from_line_invoice_ids = []
		for invoiced_sale_line_id in self.pool.get('sale.order.line').browse(cr, uid, invoiced_sale_line_ids, context=context):
			for invoice_line_id in invoiced_sale_line_id.invoice_lines:
				if invoice_line_id.invoice_id.id not in from_line_invoice_ids:
					from_line_invoice_ids.append(invoice_line_id.invoice_id.id)
		# for preinv in order.invoice_ids:
		# 	if preinv.state not in ('cancel',) and preinv.id not in from_line_invoice_ids:
		# 		for preline in preinv.invoice_line:
		# 			inv_line_id = obj_invoice_line.copy(cr, uid, preline.id, {'invoice_id': False, 'price_unit': -preline.price_unit})
		# 			print 'INV ID',inv_line_id
		# 			lines.append(inv_line_id)
		inv = self._prepare_invoice(cr, uid, order, lines, context=context)
		# print 'inv',inv
		inv_id = inv_obj.create(cr, uid, inv, context=context)
		data = inv_obj.onchange_payment_term_date_invoice(cr, uid, [inv_id], inv['payment_term'], time.strftime(DEFAULT_SERVER_DATE_FORMAT))
		if data.get('value', False):
			inv_obj.write(cr, uid, [inv_id], data['value'], context=context)
		inv_obj.button_compute(cr, uid, [inv_id])
		return inv_id
sale_order_extend()

class sale_order_line_extend(osv.osv):
	_name ="sale.order.line"
	_inherit="sale.order.line"
	
	def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
		tax_obj = self.pool.get('account.tax')
		cur_obj = self.pool.get('res.currency')
		res = {}
		c = 0
		if context is None:
			context = {}
		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = {
						'price_subtotal': 0.0,
						'serial_no': 0,
						'product_uom_qty':0.0,

			}
			c = c + 1
			res[line.id]['serial_no'] = c
			res[line.id]['product_uom_qty']= line.total_weight * line.weight
			price = line.price_unit * (line.total_weight * line.weight)
			taxes = tax_obj.compute_all(cr, uid, line.tax_id, price, line.total_weight, line.product_id, line.order_id.partner_id)
			cur = line.order_id.pricelist_id.currency_id
			res[line.id]['price_subtotal'] = price#cur_obj.round(cr, uid, cur, taxes['total'])
		return res
		
	_columns ={
		'serial_no':fields.function(_amount_line, string='Sr.', type='integer',multi="sums"),
		'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account'),multi="sums"),
		'total_weight': fields.float('Quantity', digits_compute= dp.get_precision('Product UoS'), required=True),
		'weight':fields.float("KG in Bales",readonly=True, states={'draft': [('readonly', False)]}),
		'price_unit': fields.float('Price/KG', required=True, digits_compute= dp.get_precision('Product Price'), readonly=True, states={'draft': [('readonly', False)]}),
		'product_uom_qty': fields.function(_amount_line, string='Total Weight', type='float',multi="sums",store=True),
		# 'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account'),multi="sums"),

	}	
	_defaults = {
		'serial_no':1,
	}

	def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
		"""Prepare the dict of values to create the new invoice line for a
		   sales order line. This method may be overridden to implement custom
		   invoice generation (making sure to call super() to establish
		   a clean extension chain).

		   :param browse_record line: sale.order.line record to invoice
		   :param int account_id: optional ID of a G/L account to force
			   (this is used for returning products including service)
		   :return: dict of values to create() the invoice line
		"""
		res = {}
		print "LINE",line
		if not line.invoiced:
			if not account_id:
				if line.product_id:
					account_id = line.product_id.property_account_income.id
					if not account_id:
						account_id = line.product_id.categ_id.property_account_income_categ.id
					if not account_id:
						raise osv.except_osv(_('Error!'),
								_('Please define income account for this product: "%s" (id:%d).') % \
									(line.product_id.name, line.product_id.id,))
				else:
					prop = self.pool.get('ir.property').get(cr, uid,
							'property_account_income_categ', 'product.category',
							context=context)
					account_id = prop and prop.id or False
			uosqty = self._get_line_qty(cr, uid, line, context=context)
			uos_id = self._get_line_uom(cr, uid, line, context=context)
			pu = 0.0
			if uosqty:
				pu = round(line.price_unit * line.product_uom_qty / uosqty,
						self.pool.get('decimal.precision').precision_get(cr, uid, 'Product Price'))
			fpos = line.order_id.fiscal_position or False
			account_id = self.pool.get('account.fiscal.position').map_account(cr, uid, fpos, account_id)
			if not account_id:
				raise osv.except_osv(_('Error!'),
							_('There is no Fiscal Position defined or Income category account defined for default properties of Product categories.'))
			res = {'uos_id': 1, 'product_id': line.product_id.id, 'unit_price': line.price_unit, 'account_id': account_id, 'name': line.name, 'discount': 0, 't_weight': line.weight, 'account_analytic_id': line.order_id.project_id and line.order_id.project_id.id or False, 'quantity': line.total_weight}
			# res = {
			#     'name': line.name,
			#     'sequence': line.sequence,
			#     'origin': line.order_id.name,
			#     'account_id': account_id,
			#     'price_unit': pu,
			#     'quantity': uosqty,
			#     'discount': line.discount,
			#     'uos_id': uos_id,
			#     'product_id': line.product_id.id or False,
			#     'invoice_line_tax_id': [(6, 0, [x.id for x in line.tax_id])],
			#     'account_analytic_id': line.order_id.project_id and line.order_id.project_id.id or False,
			# }

		return res

sale_order_line_extend()


class celinainvoice_extend(osv.osv):

	_inherit = 'account.invoice'
	_description = 'account invoice changes'

	# def _amount_all(self, cr, uid, ids, name, args, context=None):
	# 	res = {}
	# 	for invoice in self.browse(cr, uid, ids, context=context):
	# 		res[invoice.id] = {
	# 			# 'amount_untaxed': 0.0,
	# 			# 'amount_tax': 0.0,
	# 			# 'amount_total': 0.0,
	# 			'amount_inwords_invoice' : '',
	# 		}
	# 		for line in invoice.invoice_line:
	# 			res[invoice.id]['amount_untaxed'] += line.price_subtotal
	# 		for line in invoice.tax_line:
	# 			res[invoice.id]['amount_tax'] += line.amount
	# 		res[invoice.id]['amount_total'] = res[invoice.id]['amount_tax'] + res[invoice.id]['amount_untaxed']
	# 		amount_words = amount_to_text_en.amount_to_text(res[invoice.id]['amount_total'], 'en', 'INR')
	# 		amount_words_new = re.match( r'(.*)INR(.*?) .*', amount_words, re.M|re.I)
	# 		res[invoice.id]['amount_inwords_invoice'] = amount_words_new.group(1)
	# 	return res
	_columns ={
		# 'amount_inwords_invoice': fields.function(_amount_all, string='Amount in words',type='char',multi="sums",size=260),
		# 'amount_inwords_invoice' : fields.char('Amount in words'),
		'validity_new_invoice': fields.char("Container No."),
		'warranty_new_invoice': fields.char("Seal No."),
		'availability_new_invoice': fields.char("Availability"),
		
	}

	def write(self,cr,uid,ids,vals,context=None):
		print vals
		return super(celinainvoice_extend,self).write(cr,uid,ids,vals,context=None)
celinainvoice_extend()




