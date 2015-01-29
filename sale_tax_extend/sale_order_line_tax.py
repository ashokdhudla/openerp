from openerp.osv import fields, osv
from openerp.tools.float_utils import float_round
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp import pooler
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import openerp.addons.decimal_precision as dp
from openerp import netsvc

class sale_order_tax_computation(osv.osv):
	_inherit="sale.order"
	
	def _amount_line_tax(self, cr, uid, line, context=None):
		val = {'vat':0.0,'service':0.0}
		tax_obj = self.pool.get('account.tax')
		if line.cst_vat_tax:
			tax = tax_obj.search(cr,uid,[('name','=',line.cst_vat_tax)])
			tax_object = tax_obj.browse(cr,uid,tax)
			for c in tax_obj.compute_all(cr, uid, tax_object,line.price_unit * (1-(line.discount or 0.0)/100.0), line.product_uom_qty, line.product_id, line.order_id.partner_id)['taxes']:
				val['vat'] += c.get('amount', 0.0)
				print val['vat']
		if line.service_tax:
			tax = tax_obj.search(cr,uid,[('name','=',line.service_tax)])
			tax_object = tax_obj.browse(cr,uid,tax)
			for c in tax_obj.compute_all(cr, uid, tax_object,line.price_unit * (1-(line.discount or 0.0)/100.0), line.product_uom_qty, line.product_id, line.order_id.partner_id)['taxes']:
				val['service'] += c.get('amount', 0.0)
				print val['service']
		if line.cst_vat_tax == False and line.service_tax == False :
			print val
			return val
		#else:
			#for c in tax_obj.compute_all(cr, uid, line.tax_id,line.price_unit * (1-(line.discount or 0.0)/100.0), line.product_uom_qty, line.product_id, line.order_id.partner_id)['taxes']:
				#val += c.get('amount', 0.0)
		print val
		return val

	def _amount_all_new(self, cr, uid, ids, field_name, arg, context=None):
		cur_obj = self.pool.get('res.currency')
		tax_obj = self.pool.get('account.tax')
		res = {}
		
		for order in self.browse(cr, uid, ids, context=context):
			res[order.id] = {
				'amount_untaxed': 0.0,
				'amount_vat_cst_tax': 0.0,
				'amount_service_tax': 0.0,
				'amount_total': 0.0,
				'discount_new':0.0,
				'order_total_price':0.0,
			}
			
			val = val2 = val3 = val4 = val5 = 0.0
			print val,val5
			cur = order.pricelist_id.currency_id
			for line in order.order_line:
				val4 += line.price_subtotal
				val3 += line.price_amount
				val2 += line.price_unit * line.product_uom_qty
				#val += self._amount_line_tax(cr, uid, line, context=context)
				if line.cst_vat_tax:
					if line.cst_vat_tax != False:
						#tax = tax_obj.search(cr,uid,[('name','=',line.cst_vat_tax)])
						#tax_object = tax_obj.browse(cr,uid,line.cst_vat_tax)
						for c in tax_obj.compute_all(cr, uid,[line.cst_vat_tax],line.price_unit * (1-(line.discount or 0.0)/100.0), line.product_uom_qty, line.product_id, line.order_id.partner_id)['taxes']:
							val += c.get('amount', 0.0)
						res[order.id]['amount_vat_cst_tax'] = cur_obj.round(cr, uid, cur, val)
					print ('Vat/Cst Tax'),res[order.id]['amount_vat_cst_tax']
				if line.service_tax:
					if line.service_tax != False:
						#tax_object = tax_obj.browse(cr,uid,line.service_tax)
						for c in tax_obj.compute_all(cr, uid,[line.service_tax],line.price_unit * (1-(line.discount or 0.0)/100.0), line.product_uom_qty, line.product_id, line.order_id.partner_id)['taxes']:
							val5 += c.get('amount', 0.0)
						res[order.id]['amount_service_tax'] = cur_obj.round(cr, uid, cur, val5)
					print ('Service Tax'),res[order.id]['amount_service_tax']
				if line.cst_vat_tax == False and line.service_tax == False :
					res[order.id]['amount_vat_cst_tax'] = cur_obj.round(cr, uid, cur, val) 
					res[order.id]['amount_service_tax'] = cur_obj.round(cr, uid, cur, val5)
			res[order.id]['amount_untaxed']= cur_obj.round(cr, uid, cur, val2)
			res[order.id]['amount_total'] = cur_obj.round(cr, uid, cur, val3)
			res[order.id]['order_total_price'] = cur_obj.round(cr, uid, cur, val4)
			res[order.id]['discount_new'] = ((res[order.id]['amount_untaxed']-res[order.id]['order_total_price'])/res[order.id]['amount_untaxed'])*100
		return res
	def _get_order(self, cr, uid, ids, context=None):
		result = {}
		for line in self.pool.get('sale.order.line').browse(cr, uid, ids, context=context):
		    result[line.order_id.id] = True
		    print result.keys()

		return result.keys()

	_columns = {
		'contact_person':fields.many2one('res.partner','Contact Person',select=True),
		'amount_untaxed': fields.function(_amount_all_new, digits_compute=dp.get_precision('Account'), string='Subtotal',
			store={
				'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
		        	'sale.order.line': (_get_order, ['price_unit','discount','cst_vat_tax','service_tax', 'product_uom_qty'], 10),
		    	},
			multi='sums', help="The amount without tax.", track_visibility='always'),
		'amount_vat_cst_tax': fields.function(_amount_all_new, digits_compute=dp.get_precision('Account'), string='VAT Total',
			store={
		        	'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
		        	'sale.order.line': (_get_order, ['price_unit','discount','cst_vat_tax','service_tax', 'product_uom_qty'], 10),
		    	},
		    	multi='sums', help="The  VAT/CST tax amount."),
		'amount_service_tax': fields.function(_amount_all_new, digits_compute=dp.get_precision('Account'), string='Service Tax Total',
			store={
		        	'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
		        	'sale.order.line': (_get_order, ['price_unit','discount', 'cst_vat_tax','service_tax','product_uom_qty'], 10),
		    	},
		    	multi='sums', help="The Service tax amount."),
		'amount_total': fields.function(_amount_all_new, digits_compute=dp.get_precision('Account'), string='Grand Total',
			store={
		        	'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
		        	'sale.order.line': (_get_order, ['price_unit', 'discount', 'cst_vat_tax','service_tax','product_uom_qty'], 10),
		    	},
		    	multi='sums', help="The total amount."),
		'discount_new': fields.function(_amount_all_new, digits_compute=dp.get_precision('Account'), string='Discount',
            		store={
                		'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                		'sale.order.line': (_get_order, ['price_unit', 'discount','cst_vat_tax','service_tax', 'product_uom_qty'], 10),
            	   	},
		   	multi='sums', help="The tax amount."),
		'order_total_price': fields.function(_amount_all_new, digits_compute=dp.get_precision('Account'), string='Total Price',
            		store={
                		'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                		'sale.order.line': (_get_order, ['price_unit', 'discount','cst_vat_tax','service_tax', 'product_uom_qty'], 10),
            	   	},
		   	multi='sums', help="The Total Price."),
			
	}

	def onchange_partner_id(self, cr, uid, ids, part, context=None):
		if not part:
			return {'value': {'partner_invoice_id': False, 'partner_shipping_id': False,  'payment_term': False, 'fiscal_position': False,'contact_person':False}}

		part = self.pool.get('res.partner').browse(cr, uid, part, context=context)
		addr = self.pool.get('res.partner').address_get(cr, uid, [part.id], ['delivery', 'invoice', 'contact'])
		pricelist = part.property_product_pricelist and part.property_product_pricelist.id or False
		payment_term = part.property_payment_term and part.property_payment_term.id or False
		fiscal_position = part.property_account_position and part.property_account_position.id or False
		dedicated_salesman = part.user_id and part.user_id.id or uid
		contact_person_id = self.pool.get('res.partner').search(cr,uid,[('parent_id', '=',part.id)])
		contact_person_name= self.pool.get('res.partner').browse(cr,uid,contact_person_id)
		if contact_person_name:
			val = {
				'partner_invoice_id': addr['invoice'],
				'partner_shipping_id': addr['delivery'],
				'payment_term': payment_term,
				'fiscal_position': fiscal_position,
				'user_id': dedicated_salesman,
				'contact_person':contact_person_name[0].id,
				}
		else:
			 raise osv.except_osv(_('No Contact Person Defined!'),_("You must first create a contact person for this customer") )
		if pricelist:
			val['pricelist_id'] = pricelist
		return {'value': val}
		
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
		if context is None:
			context = {}
		journal_ids = self.pool.get('account.journal').search(cr, uid,
			[('type', '=', 'sale'), ('company_id', '=', order.company_id.id)],
			limit=1)
		if not journal_ids:
			raise osv.except_osv(_('Error!'),
				_('Please define sales journal for this company: "%s" (id:%d).') % (order.company_id.name, order.company_id.id))
		invoice_vals = {
			'name': order.client_order_ref or '',
			'origin': order.name,
			'type': 'out_invoice',
			'reference': order.client_order_ref or order.name,
			'account_id': order.partner_id.property_account_receivable.id,
			'partner_id': order.partner_invoice_id.id,
			'contact_person': order.contact_person.id,
			'journal_id': journal_ids[0],
			'invoice_line': [(6, 0, lines)],
			'currency_id': order.pricelist_id.currency_id.id,
			'comment': order.note,
			'payment_term': order.payment_term and order.payment_term.id or False,
			'fiscal_position': order.fiscal_position.id or order.partner_id.property_account_position.id,
			'date_invoice': context.get('date_invoice', False),
			'company_id': order.company_id.id,
			'user_id': order.user_id and order.user_id.id or False
		}

        # Care for deprecated _inv_get() hook - FIXME: to be removed after 6.1
		invoice_vals.update(self._inv_get(cr, uid, order, context=context))
		return invoice_vals
			
sale_order_tax_computation()

class tax_fields(osv.osv):
	_inherit='sale.order.line'
	def _amount_line_new(self, cr, uid, ids, field_name, arg, context=None):
		tax_obj = self.pool.get('account.tax')
		cur_obj = self.pool.get('res.currency')
		res = {}
		if context is None:
			context = {}
		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = {
                		'price_subtotal': 0.0,
                		'price_amount': 0.0,
           	}
			price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
			taxes = tax_obj.compute_all(cr, uid, line.tax_id, price, line.product_uom_qty, line.product_id, line.order_id.partner_id)
			cur = line.order_id.pricelist_id.currency_id
			res[line.id]['price_subtotal'] = cur_obj.round(cr, uid, cur, taxes['total'])
			total_equal1 = total_equal2 = total_equal3 =  0.0
			val1 = val2 = 0.0
			if line.cst_vat_tax:
				price = res[line.id]['price_subtotal']
				taxes = tax_obj.compute_all(cr, uid,[line.cst_vat_tax], price,line.product_uom_qty, line.product_id, line.order_id.partner_id)
				val1 = taxes['taxes'][0]['amount']

			if line.service_tax:
				price = res[line.id]['price_subtotal']
				taxes = tax_obj.compute_all(cr, uid,[line.service_tax], price,line.product_uom_qty, line.product_id, line.order_id.partner_id)
				val2 = taxes['taxes'][0]['amount']
			if  line.cst_vat_tax == False and line.service_tax == False:
				total_equal3 = res[line.id]['price_subtotal']
			if line.installation_price:
				res[line.id]['price_amount'] = cur_obj.round(cr, uid, cur, (res[line.id]['price_subtotal']+ val2 + val1 + line.installation_price))
				
			else:
				res[line.id]['price_amount'] = cur_obj.round(cr, uid, cur, res[line.id]['price_subtotal']+ val2 + val1)
				
			
		return res
		
	_columns = {
    		'price_subtotal': fields.function(_amount_line_new, string='Total Price', digits_compute= dp.get_precision('Account'),multi='sums'),
		'price_amount': fields.function(_amount_line_new, string='Total Amount', digits_compute= dp.get_precision('Account'),multi='sums'),
		'cst_vat_tax':fields.many2one('account.tax','CST/VAT'),
		'service_tax':fields.many2one('account.tax','Service Tax'),
		'installation_price':fields.float('Installation Price',digits_compute= dp.get_precision('Discount'),help="The Installation Price"),
	}
	_defaults={
	   'installation_price':0.0,
	}
	
	def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
			uom=False, qty_uos=0, uos=False, name='', partner_id=False,
			lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
		context = context or {}
		lang = lang or context.get('lang',False)
		if not partner_id:
			raise osv.except_osv(_('No Customer Defined!'), _('Before choosing a product,\n select a customer in the sales form.'))
		warning = {}
		product_uom_obj = self.pool.get('product.uom')
		partner_obj = self.pool.get('res.partner')
		product_obj = self.pool.get('product.product')
		tax_obj = self.pool.get('account.tax')
		partner = partner_obj.browse(cr, uid, partner_id).category_id
		context = {'lang': lang, 'partner_id': partner_id}
		if partner_id:
			lang = partner_obj.browse(cr, uid, partner_id).lang
		context_partner = {'lang': lang, 'partner_id': partner_id}

		if not product:
			return {'value': {'th_weight': 0,
				'product_uos_qty': qty}, 'domain': {'product_uom': [],
				'product_uos': []}}
		if not date_order:
			date_order = time.strftime(DEFAULT_SERVER_DATE_FORMAT)

		result = {}
		warning_msgs = ''
		product_obj = product_obj.browse(cr, uid, product, context=context_partner)
		if product_obj.service_tax.id:
			service_tax_obj = tax_obj.browse(cr, uid, product_obj.service_tax.id,context=context)
			result.update({'service_tax':service_tax_obj.id})
		if product_obj.cst_vat_tax.id:
			vat_tax_obj = tax_obj.browse(cr, uid, product_obj.cst_vat_tax.id,context=context)
			result.update({'cst_vat_tax':vat_tax_obj.id})
		
			
		uom2 = False
		if uom:
			uom2 = product_uom_obj.browse(cr, uid, uom)
			if product_obj.uom_id.category_id.id != uom2.category_id.id:
				uom = False
		if uos:
			if product_obj.uos_id:
				uos2 = product_uom_obj.browse(cr, uid, uos)
				if product_obj.uos_id.category_id.id != uos2.category_id.id:
					uos = False
			else:
				uos = False
		fpos = fiscal_position and self.pool.get('account.fiscal.position').browse(cr, uid, fiscal_position) or False
		if update_tax: #The quantity only have changed
			result['tax_id'] = self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, product_obj.taxes_id)

		if not flag:
			result['name'] = self.pool.get('product.product').name_get(cr, uid, [product_obj.id], context=context_partner)[0][1]
			if product_obj.description_sale:
				result['name'] += '\n'+product_obj.description_sale
		domain = {}
		if (not uom) and (not uos):
			result['product_uom'] = product_obj.uom_id.id
			if product_obj.uos_id:
				result['product_uos'] = product_obj.uos_id.id
				result['product_uos_qty'] = qty * product_obj.uos_coeff
				uos_category_id = product_obj.uos_id.category_id.id
			else:
				result['product_uos'] = False
				result['product_uos_qty'] = qty
				uos_category_id = False
			result['th_weight'] = qty * product_obj.weight
			domain = {'product_uom':
						[('category_id', '=', product_obj.uom_id.category_id.id)],
						'product_uos':
						[('category_id', '=', uos_category_id)]}
		elif uos and not uom: # only happens if uom is False
			result['product_uom'] = product_obj.uom_id and product_obj.uom_id.id
			result['product_uom_qty'] = qty_uos / product_obj.uos_coeff
			result['th_weight'] = result['product_uom_qty'] * product_obj.weight
		elif uom: # whether uos is set or not
			default_uom = product_obj.uom_id and product_obj.uom_id.id
			q = product_uom_obj._compute_qty(cr, uid, uom, qty, default_uom)
			if product_obj.uos_id:
				result['product_uos'] = product_obj.uos_id.id
				result['product_uos_qty'] = qty * product_obj.uos_coeff
			else:
				result['product_uos'] = False
				result['product_uos_qty'] = qty
			result['th_weight'] = q * product_obj.weight        # Round the quantity up

		if not uom2:
			uom2 = product_obj.uom_id
        # get unit price

		if not pricelist:
			warn_msg = _('You have to select a pricelist or a customer in the sales form !\n'
					'Please set one before choosing a product.')
			warning_msgs += _("No Pricelist ! : ") + warn_msg +"\n\n"
		else:
			price = self.pool.get('product.pricelist').price_get(cr, uid, [pricelist],
					product, qty or 1.0, partner_id, {
						'uom': uom or result.get('product_uom'),
						'date': date_order,
						})[pricelist]
			if price is False:
				warn_msg = _("Cannot find a pricelist line matching this product and quantity.\n"
						"You have to change either the product, the quantity or the pricelist.")

				warning_msgs += _("No valid pricelist line found ! :") + warn_msg +"\n\n"
			else:
				if partner:
					if partner[0].name.lower()=='customer':
						result.update({'price_unit': product_obj.list_price})
						
					elif partner[0].name.lower() =='reseller':
						result.update({'price_unit':product_obj.reseller_sale_price})
				else:
					 raise osv.except_osv(_('Tag is wrongly configured'),_("You must create a Tag for this customer, Tag must be a Customer or Reseller") )

		if warning_msgs:
			warning = {
					'title': _('Configuration Error!'),
					'message' : warning_msgs
					}
		return {'value': result, 'domain': domain, 'warning': warning}
	
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
			res = {
				'name': line.name,
				'sequence': line.sequence,
				'origin': line.order_id.name,
				'account_id': account_id,
				'price_unit': pu,
				'quantity': uosqty,
				'discount': line.discount,
				'uos_id': uos_id,
				'product_id': line.product_id.id or False,
				'cst_vat_tax': line.cst_vat_tax.id,
				'service_tax': line.service_tax.id,
				'price_subtotal': line.price_subtotal,
				'price_amount': line.price_amount,
				'installation_price': line.installation_price,
				'account_analytic_id': line.order_id.project_id and line.order_id.project_id.id or False,
			}

		return res
		
	def invoice_line_create(self, cr, uid, ids, context=None):
		if context is None:
			context = {}

		create_ids = []
		sales = set()
		for line in self.browse(cr, uid, ids, context=context):
			vals = self._prepare_order_line_invoice_line(cr, uid, line, False, context)
			if vals:
				inv_id = self.pool.get('account.invoice.line').create(cr, uid, vals, context=context)
				self.write(cr, uid, [line.id], {'invoice_lines': [(4, inv_id)]}, context=context)
				sales.add(line.order_id.id)
				create_ids.append(inv_id)
        # Trigger workflow events
		wf_service = netsvc.LocalService("workflow")
		for sale_id in sales:
			wf_service.trg_write(uid, 'sale.order', sale_id, cr)
		return create_ids
	
tax_fields()
