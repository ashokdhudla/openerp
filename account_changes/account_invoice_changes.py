import time
from lxml import etree
import openerp.addons.decimal_precision as dp
import openerp.exceptions
from openerp import tools
from openerp import netsvc
from openerp import pooler
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from openerp.tools import float_compare

class invoice_modification(osv.osv):
	"""
	Product additional fields.
	"""
	_inherit = 'account.invoice'


	def _amount_all(self, cr, uid, ids, name, args, context=None):
			# print ids
			# val1 = val2 = 0.0
			# res = {}
			# for invoice in self.browse(cr, uid, ids, context=context):
			# 	res[invoice.id] = {
			# 		'amount_untaxed': 0.0,
			# 		'amount_tax': 0.0,
			# 		'amount_total': 0.0,
			# 		'total_balance': 0.0,
			# 		'prev_balance':0.0,
			# 	}
			# 	p_ids = self.search(cr,uid,[('partner_id','=',invoice.partner_id.id)])
			# 	for i in self.browse(cr,uid,p_ids):
			# 		val1 += i.residual
			# 	p_obj = self.pool.get('res.partner').browse(cr,uid,invoice.partner_id.id)
			# 	if p_obj.supplier == True:
			# 		for line in invoice.invoice_line:
			# 			res[invoice.id]['amount_untaxed'] += line.price_subtotal
			# 		for line in invoice.tax_line:
			# 			res[invoice.id]['amount_tax'] += line.amount
			# 		res[invoice.id]['amount_total'] = res[invoice.id]['amount_tax'] + res[invoice.id]['amount_untaxed']

			# 		for line in invoice.product_line:
			# 			res[invoice.id]['amount_untaxed'] += line.price_subtotal
			# 		for line in invoice.tax_line:
			# 			res[invoice.id]['amount_tax'] += line.amount
					
			# 		res[invoice.id]['amount_total'] = res[invoice.id]['amount_untaxed']
			# 	if p_obj.supplier == False:
			# 		for line in invoice.invoice_line:
			# 			res[invoice.id]['amount_untaxed'] += line.price_subtotal_new
			# 		# for line in invoice.tax_line:
			# 		# 	res[invoice.id]['amount_tax'] += line.amount
			# 		# res[invoice.id]['amount_total'] = res[invoice.id]['amount_tax'] + res[invoice.id]['amount_untaxed']
					
			# 			res[invoice.id]['amount_total'] += line.price_subtotal_new
			# 			res[invoice.id]['prev_balance'] = val1
			# 			res[invoice.id]['total_balance'] = val1+res[invoice.id]['amount_total']
			# print res
			# return res
			
			val1 = val2 = 0.0
			res = {}
			for invoice in self.browse(cr, uid, ids, context=context):
				res[invoice.id] = {
					'amount_untaxed': 0.0,
					'amount_tax': 0.0,
					'amount_total': 0.0,
					'total_balance': 0.0,
					'prev_balance':0.0,
				}
				p_ids = self.search(cr,uid,[('partner_id','=',invoice.partner_id.id)])
				for i in self.browse(cr,uid,p_ids):
					val1 += i.residual
				p_obj = self.pool.get('res.partner').browse(cr,uid,invoice.partner_id.id)
				if p_obj.supplier == True:
					for line in invoice.invoice_line:
						if p_obj.customer == True and line.price_subtotal_new > 1.0:
							print "supplier and customer ==True"
							res[invoice.id]['amount_untaxed'] += line.price_subtotal_new
						else:
							res[invoice.id]['amount_untaxed'] += line.price_subtotal
					for line in invoice.tax_line:
						res[invoice.id]['amount_tax'] += line.amount
					res[invoice.id]['amount_total'] = res[invoice.id]['amount_tax'] + res[invoice.id]['amount_untaxed']

					for line in invoice.product_line:
						res[invoice.id]['amount_untaxed'] += line.price_subtotal
					for line in invoice.tax_line:
						res[invoice.id]['amount_tax'] += line.amount
					
					res[invoice.id]['amount_total'] = res[invoice.id]['amount_untaxed']
					print "amount total",res[invoice.id]['amount_untaxed']
				if p_obj.supplier == False:
					for line in invoice.invoice_line:
						res[invoice.id]['amount_untaxed'] += line.price_subtotal_new
					# for line in invoice.tax_line:
					# 	res[invoice.id]['amount_tax'] += line.amount
					# res[invoice.id]['amount_total'] = res[invoice.id]['amount_tax'] + res[invoice.id]['amount_untaxed']
					
						res[invoice.id]['amount_total'] += line.price_subtotal_new
						res[invoice.id]['prev_balance'] = val1
						res[invoice.id]['total_balance'] = val1+res[invoice.id]['amount_total']
					print "supplier false"
			print res
			return res


	def _amount_residual(self, cr, uid, ids, name, args, context=None):
		"""Function of the field residual. It computes the residual amount (balance) for each invoice"""
		if context is None:
			context = {}
		ctx = context.copy()
		result = {}
		currency_obj = self.pool.get('res.currency')
		for invoice in self.browse(cr, uid, ids, context=context):
			nb_inv_in_partial_rec = max_invoice_id = 0
			result[invoice.id] = 0.0
			if invoice.move_id:
				for aml in invoice.move_id.line_id:
					if aml.account_id.type in ('receivable','payable'):
						if aml.currency_id and aml.currency_id.id == invoice.currency_id.id:
							result[invoice.id] += aml.amount_residual_currency
							
						else:
							ctx['date'] = aml.date
							result[invoice.id] += currency_obj.compute(cr, uid, aml.company_id.currency_id.id, invoice.currency_id.id, aml.amount_residual, context=ctx)
							print result[invoice.id]
						if aml.reconcile_partial_id.line_partial_ids:
							#we check if the invoice is partially reconciled and if there are other invoices
							#involved in this partial reconciliation (and we sum these invoices)
							for line in aml.reconcile_partial_id.line_partial_ids:
								if line.invoice:
									nb_inv_in_partial_rec += 1
									#store the max invoice id as for this invoice we will make a balance instead of a simple division
									max_invoice_id = max(max_invoice_id, line.invoice.id)
			if nb_inv_in_partial_rec:
				#if there are several invoices in a partial reconciliation, we split the residual by the number
				#of invoice to have a sum of residual amounts that matches the partner balance
				new_value = currency_obj.round(cr, uid, invoice.currency_id, result[invoice.id] / nb_inv_in_partial_rec)
				if invoice.id == max_invoice_id:
					#if it's the last the invoice of the bunch of invoices partially reconciled together, we make a
					#balance to avoid rounding errors
					result[invoice.id] = result[invoice.id] - ((nb_inv_in_partial_rec - 1) * new_value)
				else:
					result[invoice.id] = new_value

			#prevent the residual amount on the invoice to be less than 0
			result[invoice.id] = max(result[invoice.id], 0.0)
		# print result            
		return result

	def _get_invoice_line(self, cr, uid, ids, context=None):
		result = {}
		for line in self.pool.get('account.invoice.line').browse(cr, uid, ids, context=context):
			result[line.invoice_id.id] = True
		return result.keys()

	def _get_invoice_tax(self, cr, uid, ids, context=None):
		result = {}
		for tax in self.pool.get('account.invoice.tax').browse(cr, uid, ids, context=context):
			result[tax.invoice_id.id] = True
		return result.keys()

	def _compute_lines(self, cr, uid, ids, name, args, context=None):
		result = {}
		for invoice in self.browse(cr, uid, ids, context=context):
			src = []
			lines = []
			if invoice.move_id:
				for m in invoice.move_id.line_id:
					temp_lines = []
					if m.reconcile_id:
						temp_lines = map(lambda x: x.id, m.reconcile_id.line_id)
					elif m.reconcile_partial_id:
						temp_lines = map(lambda x: x.id, m.reconcile_partial_id.line_partial_ids)
					lines += [x for x in temp_lines if x not in lines]
					src.append(m.id)

			lines = filter(lambda x: x not in src, lines)
			result[invoice.id] = lines
		return result

	def _get_lines(self, cr, uid, ids, name, arg, context=None):
		res = {}
		for invoice in self.browse(cr, uid, ids, context=context):
			id = invoice.id
			res[id] = []
			if not invoice.move_id:
				continue
			data_lines = [x for x in invoice.move_id.line_id if x.account_id.id == invoice.account_id.id]
			partial_ids = []
			for line in data_lines:
				ids_line = []
				if line.reconcile_id:
					ids_line = line.reconcile_id.line_id
				elif line.reconcile_partial_id:
					ids_line = line.reconcile_partial_id.line_partial_ids
				l = map(lambda x: x.id, ids_line)
				partial_ids.append(line.id)
				res[id] =[x for x in l if x <> line.id and x not in partial_ids]
		return res

	def _get_invoice_from_line(self, cr, uid, ids, context=None):
		move = {}
		for line in self.pool.get('account.move.line').browse(cr, uid, ids, context=context):
			if line.reconcile_partial_id:
				for line2 in line.reconcile_partial_id.line_partial_ids:
					move[line2.move_id.id] = True
			if line.reconcile_id:
				for line2 in line.reconcile_id.line_id:
					move[line2.move_id.id] = True
		invoice_ids = []
		if move:
			invoice_ids = self.pool.get('account.invoice').search(cr, uid, [('move_id','in',move.keys())], context=context)
		return invoice_ids

	def _get_invoice_from_reconcile(self, cr, uid, ids, context=None):
		move = {}
		for r in self.pool.get('account.move.reconcile').browse(cr, uid, ids, context=context):
			for line in r.line_partial_ids:
				move[line.move_id.id] = True
			for line in r.line_id:
				move[line.move_id.id] = True

		invoice_ids = []
		if move:
			invoice_ids = self.pool.get('account.invoice').search(cr, uid, [('move_id','in',move.keys())], context=context)
		print invoice_ids
		return invoice_ids

	_columns={
		'prod_type':fields.many2many('product.category','invoice_order_product_rel','charge_id','id','Type of Product'),
		'job_no':fields.char('Job Number',size=30),
		'job_date':fields.date('Job Date'),
		'master_no':fields.char('Master Number', size=30),
		'house_no':fields.char('House Number', size=30),
		'no_pack':fields.integer('Number Of Packs'),
		'weight':fields.integer("Wieght(Kgs)"),
		'vol':fields.integer('volume(CBM)'),
		'port_origin':fields.char('Port Of Origin',size=64),
		'destin':fields.char('Destination',size=64),
		'vissle':fields.char('Vessel',size=30),
		'voyage_no':fields.char('Voyage Number', size=20),
		'ship_ref':fields.char('Shipper Ref.NO',size=30),
		'eta':fields.date('ETA'),
		'etd':fields.date('ETD'),
		'charge_line':fields.one2many('account.invoice.line','charge_id','Charge Lines'),
		'product_line':fields.one2many('account.invoice.line','pr_id','Product Lines'),
		'container_no':fields.char('Container No'),
		'seal_no':fields.char('Seal No'),
		'amount_untaxed': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Subtotal', track_visibility='always',
			store={
				'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['product_line','invoice_line'], 20),
				'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount','invoice_id','pr_id'], 20),
			},
			multi='all'),
		'amount_tax': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Tax',
			store={
				'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['product_line','invoice_line'], 20),
				'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount','invoice_id','pr_id'], 20),
			},
			multi='all'),
		'amount_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total',
			store={
				'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['product_line'], 20),
				'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount','invoice_id','pr_id'], 20),
			},
			multi='all'),

		'residual': fields.function(_amount_residual, digits_compute=dp.get_precision('Account'), string='Balance',
			store={
				'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line','move_id','product_line'], 50),
				'account.invoice.tax': (_get_invoice_tax, None, 50),
				'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount','invoice_id','pr_id'], 50),
				'account.move.line': (_get_invoice_from_line, None, 50),
				'account.move.reconcile': (_get_invoice_from_reconcile, None, 50),
			},
			help="Remaining amount due."),
		'prev_balance':fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Prev Balance', track_visibility='always',
			store={
				'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['product_line','invoice_line'], 20),
				'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount','invoice_id','pr_id'], 20),
			},
			multi='all'),
		'total_balance':fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total Balance', track_visibility='always',
			store={
				'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['product_line','invoice_line'], 20),
				'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount','invoice_id','pr_id'], 20),
			},
			multi='all'),
		
	}
	def create(self,cr,uid,vals,context=None):

		return super(invoice_modification,self).create(cr,uid,vals,context=context)

	def button_reset_taxes(self, cr, uid, ids, context=None):
		if context is None:
			context = {}
		ctx = context.copy()
		ait_obj = self.pool.get('account.invoice.tax')
		for id in ids:
			cr.execute("DELETE FROM account_invoice_tax WHERE invoice_id=%s AND manual is False", (id,))
			partner = self.browse(cr, uid, id, context=ctx).partner_id
			if partner.lang:
				ctx.update({'lang': partner.lang})
			for taxe in ait_obj.compute(cr, uid, id, context=ctx).values():
				ait_obj.create(cr, uid, taxe)
		# Update the stored value (fields.function), so we write to trigger recompute
		self.pool.get('account.invoice').write(cr, uid, ids, {'invoice_line':[]}, context=ctx)
		return True

	def _prepare_order_line_move(self, cr, uid, order, order_line, picking_id, context=None):
		return {
			'name': order_line.name or '',
			'product_id': order_line.product_id.id,
			'product_qty': order_line.product_qty,
			'product_uos_qty': order_line.product_qty,
			'product_uom': order_line.product_uom.id,
			'product_uos': order_line.product_uom.id,
			'date': self.date_to_datetime(cr, uid, order.date_order, context),
			'date_expected': self.date_to_datetime(cr, uid, order_line.date_planned, context),
			'location_id': order.partner_id.property_stock_supplier.id,
			'location_dest_id': order.location_id.id,
			# 'picking_id': picking_id,
			'partner_id': order.dest_address_id.id or order.partner_id.id,
			'move_dest_id': order_line.move_dest_id.id,
			'state': 'draft',
			'type':'in',
			'purchase_line_id': order_line.id,
			'company_id': order.company_id.id,
			'price_unit': order_line.price_unit
		}

	def action_move_create(self, cr, uid, ids, context=None):
		"""Creates invoice related analytics and financial move lines"""
		print "hello validate function"
		todo_moves = []
		stock_move = self.pool.get('stock.move')
		ait_obj = self.pool.get('account.invoice.tax')
		cur_obj = self.pool.get('res.currency')
		period_obj = self.pool.get('account.period')
		payment_term_obj = self.pool.get('account.payment.term')
		journal_obj = self.pool.get('account.journal')
		move_obj = self.pool.get('account.move')
		a_obj = self.pool.get('account.invoice').browse(cr,uid,ids[0])
		invline_id = self.pool.get('account.invoice.line').search(cr,uid,[('pr_id','=',ids[0])])
		invoice_line_info = self.pool.get('account.invoice.line').browse(cr,uid,invline_id,context=None)
		for line_product_ids in invoice_line_info:
			product_obj = self.pool.get('product.product').browse(cr,uid,line_product_ids.prod_id.id,context=None)
			loc_src_id=self.pool.get('stock.location').search(cr,uid,[('complete_name','=',"Physical Locations / Celina Trading LLc. / Stock")])
			loc_supplier_id=self.pool.get('stock.location').search(cr,uid,[('complete_name','=',"Partner Locations / Suppliers")])
			print "company id",line_product_ids.company_id.id
			inventry_obj = self.pool.get('stock.inventory')
			inventry_line_obj = self.pool.get('stock.inventory.line')
			prod_obj_pool = self.pool.get('product.product')
			#pick_id1 = self.pool.get('stock.picking').create(cr,uid,{'type':'in','state':'draft','move_type':'direct','partner_id':a_obj.partner_id.id})
			invoice_line_data={
					'name': line_product_ids.prod_id.name,
					'product_id': line_product_ids.prod_id.id,
					'product_qty': line_product_ids.quantity,
					'product_uos_qty': line_product_ids.quantity,
					'product_uom': product_obj.uom_id.id,
					'product_uos': product_obj.uom_id.id,
					'location_id': loc_supplier_id[0],
					'location_dest_id': loc_src_id[0],
					'move_dest_id': '',
					'state': 'assigned',
					#'picking_id':pick_id1,
					'type':'in',
					'company_id': 1,
					'price_unit': line_product_ids.price_unit,
					
				}
			move = stock_move.create(cr , uid, invoice_line_data, context=context)
			# todo_moves.append(move)
			# print todo_moves
			# stock_move.action_confirm(cr, uid, todo_moves)
			wf_service = netsvc.LocalService("workflow")
			

			# search_ids = self.pool.get("stock.inventory.line").search(cr, uid,[('product_id','=',line_product_ids.prod_id.id)])
			# if search_ids:
			# 	last_id = max(search_ids)
			# 	obj = self.pool.get("stock.inventory.line").browse(cr,uid,last_id,context=context)
			# 	line_data ={
			# 		'product_qty' : obj.product_qty + line_product_ids.quantity,#data.new_quantity,
			# 		'location_id' : loc_src_id[0],#data.location_id.id,
			# 		'product_id' : line_product_ids.prod_id.id,
			# 		'product_uom' : product_obj.uom_id.id,
			# 	}
				
			# else:
			# 	line_data ={
			# 		'product_qty' : line_product_ids.quantity,#data.new_quantity,
			# 		'location_id' : loc_src_id[0],#data.location_id.id,
			# 		'product_id' : line_product_ids.prod_id.id,
			# 		'product_uom' : product_obj.uom_id.id,
					
			# 	}

				
		c=0
		loc_id= self.pool.get('stock.location').search(cr,uid,[('complete_name','=',"Partner Locations / Suppliers")])
		loc_src_id=self.pool.get('stock.location').search(cr,uid,[('complete_name','=',"Physical Locations / Celina Trading LLc. / Stock")])
		if invline_id:
			if a_obj.origin != False:
				pick_id = self.pool.get('stock.picking').search(cr,uid,[('origin','=',a_obj.origin)])[0]
			if a_obj.origin == False:
				pick_id = self.pool.get('stock.picking').create(cr,uid,{'container_no':a_obj.container_no,'seal_no':a_obj.seal_no,'type':'in','state':'draft','move_type':'direct','partner_id':a_obj.partner_id.id})
			line_obj = self.pool.get('account.invoice.line').browse(cr,uid,invline_id)
			for i in line_obj:
				if i.is_inventory==False:
					c += i.weight
				while(c)>0:
					pro_id = self.pool.get('stock.move')._default_product(cr,uid,ids,context=None)
					self.pool.get('product.product').write(cr,uid,pro_id,{'inv_weight':(i.quantity/i.weight),'price_unit':i.price_unit,'standard_price':(i.total_amount/i.weight),
					'list_price':(i.total_amount/i.weight)})
					pr_obj = self.pool.get('product.product').browse(cr,uid,pro_id)
					pr_obj1 = self.pool.get('product.product').browse(cr,uid,i.prod_id.id)
					res1 = self.pool.get('stock.move').create(cr,uid,{'broad_category':pr_obj1.name,'enbar':pr_obj.ean13,'name':pr_obj.name_template,'origin': False, 'product_uos_qty': 1, 'partner_id': a_obj.partner_id.id, 'product_id': pro_id, 'product_uom': 1, 'location_id': loc_id[0], 'company_id': 1, 'prodlot_id': False, 'location_dest_id': loc_src_id[0], 'tracking_id': False, 'product_qty': (i.quantity/i.weight), 'product_uos': False, 'type': 'in', 'picking_id': pick_id})
					c=c-1
		if context is None:
			context = {}
		for inv in self.browse(cr, uid, ids, context=context):
			if not inv.journal_id.sequence_id:
				raise osv.except_osv(_('Error!'), _('Please define sequence on the journal related to this invoice.'))
			if not inv.invoice_line and not inv.product_line:
				raise osv.except_osv(_('No Invoice Lines!'), _('Please create some invoice lines.'))
			if inv.move_id:
				continue

			ctx = context.copy()
			ctx.update({'lang': inv.partner_id.lang})
			if not inv.date_invoice:
				self.write(cr, uid, [inv.id], {'date_invoice': fields.date.context_today(self,cr,uid,context=context)}, context=ctx)
			company_currency = self.pool['res.company'].browse(cr, uid, inv.company_id.id).currency_id.id
			# create the analytical lines
			# one move line per invoice line
			iml = self._get_analytic_lines(cr, uid, inv.id, context=ctx)
			# check if taxes are all computed
			compute_taxes = ait_obj.compute(cr, uid, inv.id, context=ctx)
			self.check_tax_lines(cr, uid, inv, compute_taxes, ait_obj)

			# I disabled the check_total feature
			group_check_total_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account', 'group_supplier_inv_check_total')[1]
			group_check_total = self.pool.get('res.groups').browse(cr, uid, group_check_total_id, context=context)
			# if group_check_total and uid in [x.id for x in group_check_total.users]:
			# 	if (inv.type in ('in_invoice', 'in_refund') and abs(inv.check_total - inv.amount_total) >= (inv.currency_id.rounding/2.0)):
			# 		raise osv.except_osv(_('Bad Total!'), _('Please verify the price of the invoice!\nThe encoded total does not match the computed total.'))

			if inv.payment_term:
				total_fixed = total_percent = 0
				for line in inv.payment_term.line_ids:
					if line.value == 'fixed':
						total_fixed += line.value_amount
					if line.value == 'procent':
						total_percent += line.value_amount
				total_fixed = (total_fixed * 100) / (inv.amount_total or 1.0)
				if (total_fixed + total_percent) > 100:
					raise osv.except_osv(_('Error!'), _("Cannot create the invoice.\nThe related payment term is probably misconfigured as it gives a computed amount greater than the total invoiced amount. In order to avoid rounding issues, the latest line of your payment term must be of type 'balance'."))

			# one move line per tax line
			iml += ait_obj.move_line_get(cr, uid, inv.id)

			entry_type = ''
			if inv.type in ('in_invoice', 'in_refund'):
				ref = inv.reference
				entry_type = 'journal_pur_voucher'
				if inv.type == 'in_refund':
					entry_type = 'cont_voucher'
			else:
				ref = self._convert_ref(cr, uid, inv.number)
				entry_type = 'journal_sale_vou'
				if inv.type == 'out_refund':
					entry_type = 'cont_voucher'

			diff_currency_p = inv.currency_id.id <> company_currency
			# create one move line for the total and possibly adjust the other lines amount
			total = 0
			total_currency = 0
			total, total_currency, iml = self.compute_invoice_totals(cr, uid, inv, company_currency, ref, iml, context=ctx)
			acc_id = inv.account_id.id

			name = inv['name'] or inv['supplier_invoice_number'] or '/'
			totlines = False
			if inv.payment_term:
				totlines = payment_term_obj.compute(cr,
						uid, inv.payment_term.id, total, inv.date_invoice or False, context=ctx)
			if totlines:
				res_amount_currency = total_currency
				i = 0
				ctx.update({'date': inv.date_invoice})
				for t in totlines:
					if inv.currency_id.id != company_currency:
						amount_currency = cur_obj.compute(cr, uid, company_currency, inv.currency_id.id, t[1], context=ctx)
					else:
						amount_currency = False

					# last line add the diff
					res_amount_currency -= amount_currency or 0
					i += 1
					if i == len(totlines):
						amount_currency += res_amount_currency

					iml.append({
						'type': 'dest',
						'name': name,
						'price': t[1],
						'account_id': acc_id,
						'date_maturity': t[0],
						'amount_currency': diff_currency_p \
								and amount_currency or False,
						'currency_id': diff_currency_p \
								and inv.currency_id.id or False,
						'ref': ref,
					})
			else:
				iml.append({
					'type': 'dest',
					'name': name,
					'price': total,
					'account_id': acc_id,
					'date_maturity': inv.date_due or False,
					'amount_currency': diff_currency_p \
							and total_currency or False,
					'currency_id': diff_currency_p \
							and inv.currency_id.id or False,
					'ref': ref
			})

			date = inv.date_invoice or time.strftime('%Y-%m-%d')

			part = self.pool.get("res.partner")._find_accounting_partner(inv.partner_id)

			line = map(lambda x:(0,0,self.line_get_convert(cr, uid, x, part.id, date, context=ctx)),iml)

			line = self.group_lines(cr, uid, iml, line, inv)

			journal_id = inv.journal_id.id
			journal = journal_obj.browse(cr, uid, journal_id, context=ctx)
			if journal.centralisation:
				raise osv.except_osv(_('User Error!'),
						_('You cannot create an invoice on a centralized journal. Uncheck the centralized counterpart box in the related journal from the configuration menu.'))

			line = self.finalize_invoice_move_lines(cr, uid, inv, line)

			move = {
				'ref': inv.reference and inv.reference or inv.name,
				'line_id': line,
				'journal_id': journal_id,
				'date': date,
				'narration': inv.comment,
				'company_id': inv.company_id.id,
			}
			period_id = inv.period_id and inv.period_id.id or False
			ctx.update(company_id=inv.company_id.id,
					   account_period_prefer_normal=True)
			if not period_id:
				period_ids = period_obj.find(cr, uid, inv.date_invoice, context=ctx)
				period_id = period_ids and period_ids[0] or False
			if period_id:
				move['period_id'] = period_id
				for i in line:
					i[2]['period_id'] = period_id

			ctx.update(invoice=inv)
			move_id = move_obj.create(cr, uid, move, context=ctx)
			new_move_name = move_obj.browse(cr, uid, move_id, context=ctx).name
			# make the invoice point to that move
			self.write(cr, uid, [inv.id], {'move_id': move_id,'period_id':period_id, 'move_name':new_move_name}, context=ctx)
			# Pass invoice in context in method post: used if you want to get the same
			# account move reference when creating the same invoice after a cancelled one:
			move_obj.post(cr, uid, [move_id], context=ctx)
		self._log_event(cr, uid, ids)
		return True




invoice_modification()


class new_supplier_invoice_line(osv.osv):

	_inherit="account.invoice.line"

	def serial_inc(self,cr,uid,ids,field_name, arg, context=None):
		res={}
		counter=0
		for i in self.browse(cr,uid,ids,context=None):
			res[i.id]={
					'serial_no_invoice':1
				}
			counter+=1
			res[i.id]['serial_no_invoice'] = counter
		return res

	

	def _amount_line_product(self, cr, uid, ids, prop, unknow_none, unknow_dict):
		res = {}
		tax_obj = self.pool.get('account.tax')
		cur_obj = self.pool.get('res.currency')
		for line in self.browse(cr, uid, ids):
			price = line.price_unit * (1-(line.discount or 0.0)/100.0)
			taxes = tax_obj.compute_all(cr, uid, line.invoice_line_tax_id, price, line.quantity, product=line.product_id, partner=line.invoice_id.partner_id)
			res[line.id] = taxes['total']
			if line.invoice_id:
				cur = line.invoice_id.currency_id
				res[line.id] = cur_obj.round(cr, uid, cur, res[line.id])
		return res


	def _amount_line_new(self, cr, uid, ids, prop, unknow_none, unknow_dict):
		tax_obj = self.pool.get('account.tax')
		cur_obj = self.pool.get('res.currency')
		res = {}
		for line in self.browse(cr, uid, ids, context=None):
			# res[line.id]['total_weight']= line.quantity * line.t_weight
			price = line.unit_price * (line.quantity * line.t_weight)
			taxes = tax_obj.compute_all(cr, uid, line.invoice_line_tax_id, price, line.quantity, product=line.product_id, partner=line.invoice_id.partner_id)
			res[line.id] = price
			if line.invoice_id:
				cur = line.invoice_id.currency_id
				res[line.id] = cur_obj.round(cr, uid, cur, res[line.id])
		return res

	def _amount_line(self, cr, uid, ids, prop, unknow_none, unknow_dict):
		res = {}
		tax_obj = self.pool.get('account.tax')
		cur_obj = self.pool.get('res.currency')
		for line in self.browse(cr, uid, ids):
			price = line.unit_price * (line.quantity * line.t_weight)
			# print price
			taxes = tax_obj.compute_all(cr, uid, line.invoice_line_tax_id, price, line.quantity, product=line.product_id, partner=line.invoice_id.partner_id)
			res[line.id] = price
			if line.invoice_id:
				cur = line.invoice_id.currency_id
				res[line.id] = cur_obj.round(cr, uid, cur, res[line.id])
		return res
	



	_columns={
	'serial_no_invoice':fields.function(serial_inc,string='Sr.No',type="integer",multi="sums" ,readonly=True),
	'name': fields.text('Description', required=True),
	'account_id': fields.many2one('account.account', 'Account', required=True, domain=[('type','<>','view'), ('type', '<>', 'closed')], help="The income or expense account related to the selected product."),
	'charge_id': fields.many2one('account.invoice', 'Invoice Reference', ondelete='cascade', select=True),
	'pr_id': fields.many2one('account.invoice', 'Invoice Reference', ondelete='cascade', select=True),
	'ch_id': fields.many2one('product.product', 'Charge Details', ondelete='set null', select=True,domain=[('is_charge','=','True')]),
	'weight':fields.float('Weight(in Kgs.)'),
	'price_subtotal_new': fields.function(_amount_line_new, string='Total Amount', type="float",
			digits_compute= dp.get_precision('Account'), store=True),
	'total_amount': fields.function(_amount_line_product, string='Total Amount', type="float",
			digits_compute= dp.get_precision('Account'), store=True),
	'prod_id': fields.many2one('product.product', 'Product Name', ondelete='set null', select=True,domain=[('is_raw_material','=','True')]),
	't_weight':fields.float("KG in Bales"),
	'quantity': fields.float('Quantity', digits_compute= dp.get_precision('Product Unit of Measure'), required=True),
	'unit_price': fields.float('Price/KG', required=True),
	'total_weight' : fields.float('Total Weight'),
	'is_inventory':fields.boolean('Is for Inventory??'),
	}
	_defaults = {
		'serial_no_invoice':1,
		'unit_price':0.0,
		'is_inventory':True,
	}

	def move_line_get(self, cr, uid, invoice_id, context=None):
		res = []
		tax_obj = self.pool.get('account.tax')
		cur_obj = self.pool.get('res.currency')
		if context is None:
			context = {}
		inv = self.pool.get('account.invoice').browse(cr, uid, invoice_id, context=context)
		company_currency = self.pool['res.company'].browse(cr, uid, inv.company_id.id).currency_id.id
		if inv.invoice_line:
			for line in inv.invoice_line:
				mres = self.move_line_get_item(cr, uid, line, context)
				if not mres:
					continue
				res.append(mres)
				tax_code_found= False
				for tax in tax_obj.compute_all(cr, uid, line.invoice_line_tax_id,
						(line.price_unit * (1.0 - (line['discount'] or 0.0) / 100.0)),
						line.quantity, line.product_id,
						inv.partner_id)['taxes']:

					if inv.type in ('out_invoice', 'in_invoice'):
						tax_code_id = tax['base_code_id']
						tax_amount = line.price_subtotal * tax['base_sign']
					else:
						tax_code_id = tax['ref_base_code_id']
						tax_amount = line.price_subtotal * tax['ref_base_sign']

					if tax_code_found:
						if not tax_code_id:
							continue
						res.append(self.move_line_get_item(cr, uid, line, context))
						res[-1]['price'] = 0.0
						res[-1]['account_analytic_id'] = False
					elif not tax_code_id:
						continue
					tax_code_found = True

					res[-1]['tax_code_id'] = tax_code_id
					res[-1]['tax_amount'] = cur_obj.compute(cr, uid, inv.currency_id.id, company_currency, tax_amount, context={'date': inv.date_invoice})
		if inv.product_line:
			for line in inv.product_line:
				mres = self.move_line_get_item(cr, uid, line, context)
				if not mres:
					continue
				res.append(mres)
				tax_code_found= False
				for tax in tax_obj.compute_all(cr, uid, line.invoice_line_tax_id,
						(line.price_unit * (1.0 - (line['discount'] or 0.0) / 100.0)),
						line.quantity, line.product_id,
						inv.partner_id)['taxes']:

					if inv.type in ('out_invoice', 'in_invoice'):
						tax_code_id = tax['base_code_id']
						tax_amount = line.price_subtotal * tax['base_sign']
					else:
						tax_code_id = tax['ref_base_code_id']
						tax_amount = line.price_subtotal * tax['ref_base_sign']

					if tax_code_found:
						if not tax_code_id:
							continue
						res.append(self.move_line_get_item(cr, uid, line, context))
						res[-1]['price'] = 0.0
						res[-1]['account_analytic_id'] = False
					elif not tax_code_id:
						continue
					tax_code_found = True

					res[-1]['tax_code_id'] = tax_code_id
					res[-1]['tax_amount'] = cur_obj.compute(cr, uid, inv.currency_id.id, company_currency, tax_amount, context={'date': inv.date_invoice})
		return res

	def change_total_weight(self, cr, uid, ids,t_weight,quantity,context=None):
		total = t_weight * quantity
		return {'value': {'total_weight': t_weight * quantity}}
		
	def move_line_get_item(self, cr, uid, line, context=None):
		if line.invoice_id:
			p_obj = self.pool.get('res.partner').browse(cr,uid,line.invoice_id.partner_id.id)
		else:
			p_obj = self.pool.get('res.partner').browse(cr,uid,line.pr_id.partner_id.id)
		if p_obj.supplier==True:
			return {
				'type':'src',
				'name': line.name.split('\n')[0][:64],
				'price_unit':line.price_unit,
				'quantity':line.quantity,
				'price':line.price_subtotal,
				'account_id':line.account_id.id,
				'product_id':line.product_id.id,
				'uos_id':line.uos_id.id,
				'account_analytic_id':line.account_analytic_id.id,
				'taxes':line.invoice_line_tax_id,
			}

		if p_obj.supplier==False:

			return {
				'type':'src',
				'name': line.name.split('\n')[0][:64],
				'price_unit':line.unit_price,
				'quantity':line.quantity,
				'price':line.price_subtotal_new,
				'account_id':line.account_id.id,
				'product_id':line.product_id.id,
				'uos_id':line.uos_id.id,
				'account_analytic_id':line.account_analytic_id.id,
				'taxes':line.invoice_line_tax_id,
			}

	def onchange_prod_id(self,cr,uid,ids,prod_id,context=None):
		result = {'value':{}}
		res = self.pool.get('product.product').browse(cr,uid,prod_id,context=None)
		result['value'].update({'name':res.name_template})
		return result

	def onchange_charge_id(self,cr,uid,ids,ch_id,context=None):
		result = {'value':{}}
		res = self.pool.get('product.product').browse(cr,uid,ch_id,context=None)
		result['value'].update({'name':res.name_template})
		return result

new_supplier_invoice_line()



class copy_debit_credit(osv.osv):

	_inherit = "account.account"


	def __compute(self, cr, uid, ids, field_names, arg=None, context=None,
				  query='', query_params=()):
		""" compute the balance, debit and/or credit for the provided
		account ids
		Arguments:
		`ids`: account ids
		`field_names`: the fields to compute (a list of any of
					   'balance', 'debit' and 'credit')
		`arg`: unused fields.function stuff
		`query`: additional query filter (as a string)
		`query_params`: parameters for the provided query string
						(__compute will handle their escaping) as a
						tuple
		"""
		mapping = {
			'balance': "COALESCE(SUM(l.debit),0) - COALESCE(SUM(l.credit), 0) as balance",
			'debit': "COALESCE(SUM(l.debit), 0) as debit",
			'credit': "COALESCE(SUM(l.credit), 0) as credit",
			# by convention, foreign_balance is 0 when the account has no secondary currency, because the amounts may be in different currencies
			'foreign_balance': "(SELECT CASE WHEN currency_id IS NULL THEN 0 ELSE COALESCE(SUM(l.amount_currency), 0) END FROM account_account WHERE id IN (l.account_id)) as foreign_balance",
		}
		#get all the necessary accounts
		children_and_consolidated = self._get_children_and_consol(cr, uid, ids, context=context)
		#compute for each account the balance/debit/credit from the move lines
		accounts = {}
		res = {}
		null_result = dict((fn, 0.0) for fn in field_names)
		if children_and_consolidated:
			aml_query = self.pool.get('account.move.line')._query_get(cr, uid, context=context)

			wheres = [""]
			if query.strip():
				wheres.append(query.strip())
			if aml_query.strip():
				wheres.append(aml_query.strip())
			filters = " AND ".join(wheres)
			# IN might not work ideally in case there are too many
			# children_and_consolidated, in that case join on a
			# values() e.g.:
			# SELECT l.account_id as id FROM account_move_line l
			# INNER JOIN (VALUES (id1), (id2), (id3), ...) AS tmp (id)
			# ON l.account_id = tmp.id
			# or make _get_children_and_consol return a query and join on that
			request = ("SELECT l.account_id as id, " +\
					   ', '.join(mapping.values()) +
					   " FROM account_move_line l" \
					   " WHERE l.account_id IN %s " \
							+ filters +
					   " GROUP BY l.account_id")
			params = (tuple(children_and_consolidated),) + query_params
			cr.execute(request, params)

			for row in cr.dictfetchall():
				accounts[row['id']] = row

			# consolidate accounts with direct children
			children_and_consolidated.reverse()
			brs = list(self.browse(cr, uid, children_and_consolidated, context=context))
			sums = {}
			currency_obj = self.pool.get('res.currency')
			while brs:
				current = brs.pop(0)
#                can_compute = True
#                for child in current.child_id:
#                    if child.id not in sums:
#                        can_compute = False
#                        try:
#                            brs.insert(0, brs.pop(brs.index(child)))
#                        except ValueError:
#                            brs.insert(0, child)
#                if can_compute:
				for fn in field_names:
					sums.setdefault(current.id, {})[fn] = accounts.get(current.id, {}).get(fn, 0.0)
					for child in current.child_id:
						if child.company_id.currency_id.id == current.company_id.currency_id.id:
							sums[current.id][fn] += sums[child.id][fn]
						else:
							sums[current.id][fn] += currency_obj.compute(cr, uid, child.company_id.currency_id.id, current.company_id.currency_id.id, sums[child.id][fn], context=context)

				# as we have to relay on values computed before this is calculated separately than previous fields
				if current.currency_id and current.exchange_rate and \
							('adjusted_balance' in field_names or 'unrealized_gain_loss' in field_names):
					# Computing Adjusted Balance and Unrealized Gains and losses
					# Adjusted Balance = Foreign Balance / Exchange Rate
					# Unrealized Gains and losses = Adjusted Balance - Balance
					adj_bal = sums[current.id].get('foreign_balance', 0.0) / current.exchange_rate
					sums[current.id].update({'adjusted_balance': adj_bal, 'unrealized_gain_loss': adj_bal - sums[current.id].get('balance', 0.0)})

			for id in ids:
				res[id] = sums.get(id, null_result)
		else:
			for id in ids:
				res[id] = null_result
		return res

	
	def _set_credit_debit(self, cr, uid, account_id, name, value, arg, context=None):
		if context.get('config_invisible', True):
			return True

		account = self.browse(cr, uid, account_id, context=context)
		diff = value - getattr(account,name)
		# print diff
		if not diff:
			return True

		journal_obj = self.pool.get('account.journal')
		jids = journal_obj.search(cr, uid, [('type','=','situation'),('centralisation','=',1),('company_id','=',account.company_id.id)], context=context)
		if not jids:
			raise osv.except_osv(_('Error!'),_("You need an Opening journal with centralisation checked to set the initial balance."))

		period_obj = self.pool.get('account.period')
		pids = period_obj.search(cr, uid, [('special','=',True),('company_id','=',account.company_id.id)], context=context)
		if not pids:
			raise osv.except_osv(_('Error!'),_("There is no opening/closing period defined, please create one to set the initial balance."))

		move_obj = self.pool.get('account.move.line')
		move_id = move_obj.search(cr, uid, [
			('journal_id','=',jids[0]),
			('period_id','=',pids[0]),
			('account_id','=', account_id),
			(name,'>', 0.0),
			('name','=', _('Opening Balance'))
		], context=context)
		if move_id:
			move = move_obj.browse(cr, uid, move_id[0], context=context)
			move_obj.write(cr, uid, move_id[0], {
				name: diff+getattr(move,name)
			}, context=context)
		else:
			if diff<0.0:
				raise osv.except_osv(_('Error!'),_("Unable to adapt the initial balance (negative value)."))
			nameinv = (name=='credit' and 'debit') or 'credit'
			move_id = move_obj.create(cr, uid, {
				'name': _('Opening Balance'),
				'account_id': account_id,
				'journal_id': jids[0],
				'period_id': pids[0],
				name: diff,
				nameinv: 0.0
			}, context=context)
		return True


	_columns = {
		'balance': fields.function(__compute, digits_compute=dp.get_precision('Account'), string='Balance', multi='balance'),
		'credit': fields.function(__compute, fnct_inv=_set_credit_debit, digits_compute=dp.get_precision('Account'), string='Credit', multi='balance'),
		'debit': fields.function(__compute, fnct_inv=_set_credit_debit, digits_compute=dp.get_precision('Account'), string='Debit', multi='balance'),
	}


copy_debit_credit()



class product_changes(osv.osv):

	_inherit='product.template'

	_columns = {
		'is_bale':fields.boolean('Is Bale'),
		'is_raw_material':fields.boolean('Is Raw Material'),
		'is_charge':fields.boolean('Is Charge'),
		'purchase_ok': fields.boolean('Can be Purchased', help="Specify if the product can be selected in a purchase order line."),
		'price_unit':fields.float('Product Price',digits_compute=dp.get_precision('Account')),
		'inv_weight':fields.float('Invoice Weight'),
		}

	# def create(self,cr,uid,vals,context=None):
	# 	if context != None:
	# 		if 'search_default_filter_is_charge' in context:
	# 			vals.update({'is_charge':True})

	# 	return super(product_changes,self).create(cr,uid,vals,context=context)

product_changes()


class product_type(osv.osv):

	_name="product.type"

	_columns={
		'name':fields.char('Name'),
	}

product_type()


class product_charge(osv.osv):
	"""
	Product additional fields.
	"""
	_inherit = 'product.product'

	# _columns = {
	#     'is_raw_material':fields.boolean('Is Raw Material'),
	#  	}

	# _defaults={
	# 'is_raw_material':1,
	# }

product_charge()

class account_voucher(osv.osv):
	def _get_writeoff_amount1(self, cr, uid, ids, name, args, context=None):
		print "_get_writeoff_amount1................"
		if not ids: return {}
		currency_obj = self.pool.get('res.currency')
		res = {}
		debit = credit = 0.0
		for voucher in self.browse(cr, uid, ids, context=context):
			sign = voucher.type == 'payment' and -1 or 1
			for l in voucher.line_dr_ids:
				# debit +=l.amount
				debit += l.amount1
			for l in voucher.line_cr_ids:
				# credit +=l.amount
				credit += l.amount1
			currency = voucher.currency_id or voucher.company_id.currency_id
			# print "currency",currency
			# print "voucher.amount",voucher.amount
			# print "credit",credit
			# print "debit",debit
			print "voucher.amount*voucher.payment_rate.......",round(voucher.amount*voucher.payment_rate)
			res[voucher.id] =  currency_obj.round(cr, uid, currency, round(voucher.amount*voucher.payment_rate) - sign * (credit - debit))
		return res

	def onchage_total1(self, cr, uid, ids, total1, payment_rate,context=None):
		print "payment_rate",payment_rate
		res = {}
		usd_cur = (int(total1)/payment_rate)
		res['amount'] = usd_cur
		return {'value' : res}

	def _get_journal_currency1(self, cr, uid, ids, name, args, context=None):
		print "currency_id11111111............"
		res = {}
		for voucher in self.browse(cr, uid, ids, context=context):
			res[voucher.id] = voucher.journal_id.currency and voucher.journal_id.currency.id or voucher.company_id.currency_id.id
		return res

	def _get_currency1(self, cr, uid, context=None):
		print "_get_currency11111111111"
		if context is None: context = {}
		journal_pool = self.pool.get('account.journal')
		journal_id = context.get('journal_id', False)
		if journal_id:
			journal = journal_pool.browse(cr, uid, journal_id, context=context)
			if journal.currency:
				return journal.currency.id
		print "self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.currency_id.id",self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.currency_id.id
		return self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.currency_id.id

	def _get_payment_rate_currency(self, cr, uid, context=None):
		"""
		Return the default value for field payment_rate_currency_id: the currency of the journal
		if there is one, otherwise the currency of the user's company
		"""
		if context is None: context = {}
		journal_pool = self.pool.get('account.journal')
		journal_id = context.get('journal_id', False)
		if journal_id:
			journal = journal_pool.browse(cr, uid, journal_id, context=context)
			if journal.currency:
				return journal.currency.id
		#no journal given in the context, use company currency as default
		return self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.currency_id.id

	
	_inherit = 'account.voucher'

	_columns = {
		'partner_id':fields.many2one('res.partner', 'Partner', change_default=1, readonly=True, states={'draft':[('readonly',False)]}),
		# 'amount': fields.float('Total', digits_compute=dp.get_precision('Account'), required=True, readonly=True, states={'draft':[('readonly',False)]}),
		# 'journal_id':fields.many2one('account.journal', 'Journal', required=True, readonly=True, states={'draft':[('readonly',False)]}),
		'journal_id1' : fields.many2one('payment.new','Payment method',required=True),
		'symbol' : fields.char('Symbol',size=20),
		'total1' : fields.float('Total',required=True),
		'amount_original1' : fields.char('Amount Original123'),
		'writeoff_amount1': fields.function(_get_writeoff_amount1, string='Difference Amount', type='float', readonly=True, help="Computed as the difference between the amount stated in the voucher and the sum of allocation on the voucher lines."),
		'line_dr_ids':fields.one2many('account.voucher.line','voucher_id','Debits',
			domain=[('type','=','dr')], context={'default_type':'dr'}, readonly=True, states={'draft':[('readonly',False)]}),		
		'sup_cur' : fields.char('currency'),
		'cur_id' : fields.integer('Currency id'),
		'payment_rate': fields.float('Exchange Rate', digits=(12,6), required=True, readonly=True, states={'draft': [('readonly', False)]},
			help='The specific rate that will be used, in this voucher, between the selected currency (in \'Payment Rate Currency\' field)  and the voucher currency.'),
		'payment_rate_currency_id': fields.many2one('res.currency', 'Payment Rate Currency', required=True, readonly=True, states={'draft':[('readonly',False)]}),
		# 'currency_id1': fields.function(_get_journal_currency1, type='many2one', relation='res.currency', string='Currency', readonly=True, required=True),

		# 'amount_unreconciled1' : fields.char('Open Balance'),
		# 'reconcile' : fields.boolean('Full Reconcile'),
		# 'amount1':fields.float('Amount', digits_compute=dp.get_precision('Account')),
		}
	_defaults = {
		'total1' : 0.00,
		'payment_rate': 1.0,
		'payment_rate_currency_id': _get_payment_rate_currency,
	}
	# def onchange_reconcile(self, cr, uid, ids, reconcile, amount, amount_unreconciled, amount_unreconciled1, context=None):
	# 	vals = {'amount': 0.0}
	# 	print "amount_unreconciled",amount_unreconciled
	# 	print "amount_unreconciled1",amount_unreconciled1
	# 	if reconcile:
	# 		vals = { 'amount': amount_unreconciled}
	# 		vals = { 'amount1': amount_unreconciled1}
	# 	return {'value': vals}

	def onchange_journal1(self,cr,uid,ids,journal_id1):
		res = {'value': {'journal_id': False}}
		pyt_method_obj = self.pool.get('payment.new').browse(cr,uid,journal_id1),
		for pyt_obj in pyt_method_obj:
			if "bank"in str(pyt_obj.payment_method).lower():
				voucher_ids = self.pool.get('account.journal').search(cr,uid,[('type','=','bank')],context=None)
				res['value']['journal_id'] = voucher_ids
			if "cash"in str(pyt_obj.payment_method).lower():
				voucher_ids = self.pool.get('account.journal').search(cr,uid,[('type','=','cash')],context=None)
				res['value']['journal_id'] = voucher_ids
		return res

	def basic_onchange_partner(self, cr, uid, ids, partner_id, journal_id, ttype, context=None):
		partner_pool = self.pool.get('res.partner')
		journal_pool = self.pool.get('account.journal')
		res = {'value': {'account_id': False}}
		if not partner_id or not journal_id:
			return res

		journal = journal_pool.browse(cr, uid, journal_id, context=context)
		partner = partner_pool.browse(cr, uid, partner_id, context=context)
		account_id = False
		if journal.type in ('sale','sale_refund'):
			account_id = partner.property_account_receivable.id
		elif journal.type in ('purchase', 'purchase_refund','expense'):
			account_id = partner.property_account_payable.id
		else:
			account_id = journal.default_credit_account_id.id or journal.default_debit_account_id.id

		res['value']['account_id'] = account_id
		return res

	def onchange_partner_id(self, cr, uid, ids, partner_id, journal_id, amount, currency_id, ttype, date, context=None):
		print "onchange partner id"
		if not journal_id:
			return {}
		if context is None:
			context = {}
		#TODO: comment me and use me directly in the sales/purchases views
		res = self.basic_onchange_partner(cr, uid, ids, partner_id, journal_id, ttype, context=context)
		print "partner_id",partner_id
		if partner_id:
			accnt_invoice_ids = self.pool.get('account.invoice').search(cr,uid,[('partner_id','=',partner_id)])
			if accnt_invoice_ids:
				accnt_invoice_obj = self.pool.get('account.invoice').browse(cr, uid, accnt_invoice_ids[0])
				res['value']['symbol'] = accnt_invoice_obj.currency_id.id
				res['value']['sup_cur'] = accnt_invoice_obj.currency_id.symbol
				res['value']['cur_id'] = accnt_invoice_obj.currency_id.id
		if ttype in ['sale', 'purchase']:
			return res
		ctx = context.copy()
		# not passing the payment_rate currency and the payment_rate in the context but it's ok because they are reset in recompute_payment_rate
		ctx.update({'date': date})
		vals = self.recompute_voucher_lines(cr, uid, ids, partner_id, journal_id, amount, currency_id, ttype, date, context=ctx)
		vals2 = self.recompute_payment_rate(cr, uid, ids, vals, currency_id, date, ttype, journal_id, amount, context=context)
		for key in vals.keys():
			res[key].update(vals[key])
		for key in vals2.keys():
			res[key].update(vals2[key])
		#TODO: can probably be removed now
		#TODO: onchange_partner_id() should not returns [pre_line, line_dr_ids, payment_rate...] for type sale, and not 
		# [pre_line, line_cr_ids, payment_rate...] for type purchase.
		# We should definitively split account.voucher object in two and make distinct on_change functions. In the 
		# meanwhile, bellow lines must be there because the fields aren't present in the view, what crashes if the 
		# onchange returns a value for them
		if ttype == 'sale':
			del(res['value']['line_dr_ids'])
			del(res['value']['pre_line'])
			del(res['value']['payment_rate'])
		elif ttype == 'purchase':
			del(res['value']['line_cr_ids'])
			del(res['value']['pre_line'])
			del(res['value']['payment_rate'])
		return res

	def onchange_rate(self, cr, uid, ids, rate, amount, currency_id, payment_rate_currency_id, company_id, context=None):
		res =  {'value': {'paid_amount_in_company_currency': amount, 'currency_help_label': self._get_currency_help_label(cr, uid, currency_id, rate, payment_rate_currency_id, context=context)}}
		if rate and amount and currency_id:
			company_currency = self.pool.get('res.company').browse(cr, uid, company_id, context=context).currency_id
			#context should contain the date, the payment currency and the payment rate specified on the voucher
			amount_in_company_currency = self.pool.get('res.currency').compute(cr, uid, currency_id, company_currency.id, amount, context=context)
			res['value']['paid_amount_in_company_currency'] = amount_in_company_currency
		return res

	def recompute_voucher_lines(self, cr, uid, ids, partner_id, journal_id, price, currency_id, ttype, date, context=None):
		print "recompute voucher linesss triggerrrrrrrrrrrrr"
		"""
		Returns a dict that contains new values and context

		@param partner_id: latest value from user input for field partner_id
		@param args: other arguments
		@param context: context arguments, like lang, time zone

		@return: Returns a dict which contains new values, and context
		"""
		def _remove_noise_in_o2m():
			"""if the line is partially reconciled, then we must pay attention to display it only once and
				in the good o2m.
				This function returns True if the line is considered as noise and should not be displayed
			"""
			if line.reconcile_partial_id:
				if currency_id == line.currency_id.id:
					if line.amount_residual_currency <= 0:
						return True
				else:
					if line.amount_residual <= 0:
						return True
			return False

		if context is None:
			context = {}
		context_multi_currency = context.copy()

		currency_pool = self.pool.get('res.currency')
		move_line_pool = self.pool.get('account.move.line')
		partner_pool = self.pool.get('res.partner')
		journal_pool = self.pool.get('account.journal')
		line_pool = self.pool.get('account.voucher.line')

		#set default values
		default = {
			'value': {'line_dr_ids': [] ,'line_cr_ids': [] ,'pre_line': False,},
		}

		#drop existing lines
		line_ids = ids and line_pool.search(cr, uid, [('voucher_id', '=', ids[0])]) or False
		if line_ids:
			line_pool.unlink(cr, uid, line_ids)

		if not partner_id or not journal_id:
			return default

		journal = journal_pool.browse(cr, uid, journal_id, context=context)
		partner = partner_pool.browse(cr, uid, partner_id, context=context)
		currency_id = currency_id or journal.company_id.currency_id.id

		total_credit = 0.0
		total_debit = 0.0
		account_type = 'receivable'
		if ttype == 'payment':
			account_type = 'payable'
			total_debit = price or 0.0
		else:
			total_credit = price or 0.0
			account_type = 'receivable'

		if not context.get('move_line_ids', False):
			ids = move_line_pool.search(cr, uid, [('state','=','valid'), ('account_id.type', '=', account_type), ('reconcile_id', '=', False), ('partner_id', '=', partner_id)], context=context)
		else:
			ids = context['move_line_ids']
		invoice_id = context.get('invoice_id', False)
		company_currency = journal.company_id.currency_id.id
		move_line_found = False

		#order the lines by most old first
		ids.reverse()
		account_move_lines = move_line_pool.browse(cr, uid, ids, context=context)

		#compute the total debit/credit and look for a matching open amount or invoice
		for line in account_move_lines:
			print "line debit",abs(line.amount_currency)
			if _remove_noise_in_o2m():
				continue

			if invoice_id:
				if line.invoice.id == invoice_id:
					#if the invoice linked to the voucher line is equal to the invoice_id in context
					#then we assign the amount on that line, whatever the other voucher lines
					move_line_found = line.id
					break
			elif currency_id == company_currency:
				#otherwise treatments is the same but with other field names
				if line.amount_residual == price:
					#if the amount residual is equal the amount voucher, we assign it to that voucher
					#line, whatever the other voucher lines
					move_line_found = line.id
					break
				#otherwise we will split the voucher amount on each line (by most old first)
				total_credit += line.credit or 0.0
				total_debit += line.debit or 0.0
			elif currency_id == line.currency_id.id:
				if line.amount_residual_currency == price:
					move_line_found = line.id
					break
				total_credit += line.credit and line.amount_currency or 0.0
				total_debit += line.debit and line.amount_currency or 0.0

		#voucher line creation
		for line in account_move_lines:

			if _remove_noise_in_o2m():
				continue
			if line.currency_id and currency_id == line.currency_id.id:
				amount_original = abs(line.amount_currency)
				amount_unreconciled = abs(line.amount_residual_currency)
			else:
				#always use the amount booked in the company currency as the basis of the conversion into the voucher currency
				amount_original = currency_pool.compute(cr, uid, company_currency, currency_id, line.credit or line.debit or 0.0, context=context_multi_currency)
				amount_unreconciled = currency_pool.compute(cr, uid, company_currency, currency_id, abs(line.amount_residual), context=context_multi_currency)
			line_currency_id = line.currency_id and line.currency_id.id or company_currency
			rs = {
				'name':line.move_id.name,
				'type': line.credit and 'dr' or 'cr',
				'move_line_id':line.id,
				'account_id':line.account_id.id,
				'amount_original': amount_original,
				'amount_original1' : abs(line.amount_currency),
				'amount': (move_line_found == line.id) and min(abs(price), amount_unreconciled) or 0.0,
				'date_original':line.date,
				'date_due':line.date_maturity,
				'amount_unreconciled': amount_unreconciled,
				'amount_unreconciled1' : abs(line.amount_residual_currency),
				'currency_id': line_currency_id,
			}
			#in case a corresponding move_line hasn't been found, we now try to assign the voucher amount
			#on existing invoices: we split voucher amount by most old first, but only for lines in the same currency
			if not move_line_found:
				if currency_id == line_currency_id:
					if line.credit:
						amount = min(amount_unreconciled, abs(total_debit))
						rs['amount'] = amount
						total_debit -= amount
					else:
						amount = min(amount_unreconciled, abs(total_credit))
						rs['amount'] = amount
						total_credit -= amount

			if rs['amount_unreconciled'] == rs['amount']:
				rs['reconcile'] = True

			if rs['type'] == 'cr':
				default['value']['line_cr_ids'].append(rs)
			else:
				default['value']['line_dr_ids'].append(rs)

			if ttype == 'payment' and len(default['value']['line_cr_ids']) > 0:
				default['value']['pre_line'] = 1
			elif ttype == 'receipt' and len(default['value']['line_dr_ids']) > 0:
				default['value']['pre_line'] = 1
			default['value']['writeoff_amount'] = self._compute_writeoff_amount(cr, uid, default['value']['line_dr_ids'], default['value']['line_cr_ids'], price, ttype)
		return default

	def onchange_amount(self, cr, uid, ids, amount, rate, partner_id, journal_id, currency_id, ttype, date, payment_rate_currency_id, company_id, context=None):
		if context is None:
			context = {}
		ctx = context.copy()
		ctx.update({'date': date})
		#read the voucher rate with the right date in the context
		currency_id = currency_id or self.pool.get('res.company').browse(cr, uid, company_id, context=ctx).currency_id.id
		voucher_rate = self.pool.get('res.currency').read(cr, uid, currency_id, ['rate'], context=ctx)['rate']
		ctx.update({
			'voucher_special_currency': payment_rate_currency_id,
			'voucher_special_currency_rate': rate * voucher_rate})
		res = self.recompute_voucher_lines(cr, uid, ids, partner_id, journal_id, amount, currency_id, ttype, date, context=ctx)
		vals = self.onchange_rate(cr, uid, ids, rate, amount, currency_id, payment_rate_currency_id, company_id, context=ctx)
		for key in vals.keys():
			res[key].update(vals[key])
		return res

	def onchange_journal(self, cr, uid, ids, journal_id, line_ids, tax_id, partner_id, date, amount, ttype, company_id, context=None):
		print "onchange payment method"
		if context is None:
			context = {}
		if not journal_id:
			return False
		journal_pool = self.pool.get('account.journal')
		journal = journal_pool.browse(cr, uid, journal_id, context=context)
		account_id = journal.default_credit_account_id or journal.default_debit_account_id
		tax_id = False
		if account_id and account_id.tax_ids:
			tax_id = account_id.tax_ids[0].id

		vals = {'value':{} }
		if ttype in ('sale', 'purchase'):
			vals = self.onchange_price(cr, uid, ids, line_ids, tax_id, partner_id, context)
			vals['value'].update({'tax_id':tax_id,'amount': amount})
		currency_id = False
		if journal.currency:
			currency_id = journal.currency.id
		else:
			currency_id = journal.company_id.currency_id.id
		vals['value'].update({'currency_id': currency_id})
		#in case we want to register the payment directly from an invoice, it's confusing to allow to switch the journal 
		#without seeing that the amount is expressed in the journal currency, and not in the invoice currency. So to avoid
		#this common mistake, we simply reset the amount to 0 if the currency is not the invoice currency.
		if context.get('payment_expected_currency') and currency_id != context.get('payment_expected_currency'):
			vals['value']['amount'] = 0
			amount = 0
		res = self.onchange_partner_id(cr, uid, ids, partner_id, journal_id, amount, currency_id, ttype, date, context)
		for key in res.keys():
			vals[key].update(res[key])
		return vals

	def _get_company_currency(self, cr, uid, voucher_id, context=None):
		'''
		Get the currency of the actual company.

		:param voucher_id: Id of the voucher what i want to obtain company currency.
		:return: currency id of the company of the voucher
		:rtype: int
		'''
		return self.pool.get('account.voucher').browse(cr,uid,voucher_id,context).journal_id.company_id.currency_id.id
		
	def _get_current_currency(self, cr, uid, voucher_id, context=None):
		'''
		Get the currency of the voucher.

		:param voucher_id: Id of the voucher what i want to obtain current currency.
		:return: currency id of the voucher
		:rtype: int
		'''
		voucher = self.pool.get('account.voucher').browse(cr,uid,voucher_id,context)
		return voucher.currency_id.id or self._get_company_currency(cr,uid,voucher.id,context)

	def _sel_context(self, cr, uid, voucher_id, context=None):
		"""
		Select the context to use accordingly if it needs to be multicurrency or not.

		:param voucher_id: Id of the actual voucher
		:return: The returned context will be the same as given in parameter if the voucher currency is the same
				 than the company currency, otherwise it's a copy of the parameter with an extra key 'date' containing
				 the date of the voucher.
		:rtype: dict
		"""
		company_currency = self._get_company_currency(cr, uid, voucher_id, context)
		current_currency = self._get_current_currency(cr, uid, voucher_id, context)
		if current_currency <> company_currency:
			context_multi_currency = context.copy()
			voucher = self.pool.get('account.voucher').browse(cr, uid, voucher_id, context)
			context_multi_currency.update({'date': voucher.date})
			return context_multi_currency
		return context

	def _convert_amount(self, cr, uid, amount, voucher_id, context=None):
		'''
		This function convert the amount given in company currency. It takes either the rate in the voucher (if the
		payment_rate_currency_id is relevant) either the rate encoded in the system.

		:param amount: float. The amount to convert
		:param voucher: id of the voucher on which we want the conversion
		:param context: to context to use for the conversion. It may contain the key 'date' set to the voucher date
			field in order to select the good rate to use.
		:return: the amount in the currency of the voucher's company
		:rtype: float
		'''
		if context is None:
			context = {}
		currency_obj = self.pool.get('res.currency')
		voucher = self.browse(cr, uid, voucher_id, context=context)
		return currency_obj.compute(cr, uid, voucher.currency_id.id, voucher.company_id.currency_id.id, amount, context=context)

	
	def writeoff_move_line_get(self, cr, uid, voucher_id, line_total, move_id, name, company_currency, current_currency, context=None):
		'''
		Set a dict to be use to create the writeoff move line.

		:param voucher_id: Id of voucher what we are creating account_move.
		:param line_total: Amount remaining to be allocated on lines.
		:param move_id: Id of account move where this line will be added.
		:param name: Description of account move line.
		:param company_currency: id of currency of the company to which the voucher belong
		:param current_currency: id of currency of the voucher
		:return: mapping between fieldname and value of account move line to create
		:rtype: dict
		'''
		# print "writeoff_amount................................................"
		currency_obj = self.pool.get('res.currency')
		move_line = {}

		voucher = self.pool.get('account.voucher').browse(cr,uid,voucher_id,context)
		current_currency_obj = voucher.currency_id or voucher.journal_id.company_id.currency_id

		if not currency_obj.is_zero(cr, uid, current_currency_obj, line_total):
			diff = line_total
			account_id = False
			write_off_name = ''
			if voucher.payment_option == 'with_writeoff':
				account_id = voucher.writeoff_acc_id.id
				write_off_name = voucher.comment
			elif voucher.type in ('sale', 'receipt'):
				account_id = voucher.partner_id.property_account_receivable.id
			else:
				account_id = voucher.partner_id.property_account_payable.id
			sign = voucher.type == 'payment' and -1 or 1
			move_line = {
				'name': write_off_name or name,
				'account_id': account_id,
				'move_id': move_id,
				'partner_id': voucher.partner_id.id,
				'date': voucher.date,
				'credit': diff > 0 and diff or 0.0,
				'debit': diff < 0 and -diff or 0.0,
				'amount_currency': company_currency <> current_currency and (sign * -1 * voucher.writeoff_amount) or False,
				'currency_id': company_currency <> current_currency and current_currency or False,
				'analytic_account_id': voucher.analytic_id and voucher.analytic_id.id or False,
			}
		return move_line

	def voucher_move_line_create(self, cr, uid, voucher_id, line_total, move_id, company_currency, current_currency, context=None):
		'''
		Create one account move line, on the given account move, per voucher line where amount is not 0.0.
		It returns Tuple with tot_line what is total of difference between debit and credit and
		a list of lists with ids to be reconciled with this format (total_deb_cred,list_of_lists).

		:param voucher_id: Voucher id what we are working with
		:param line_total: Amount of the first line, which correspond to the amount we should totally split among all voucher lines.
		:param move_id: Account move wher those lines will be joined.
		:param company_currency: id of currency of the company to which the voucher belong
		:param current_currency: id of currency of the voucher
		:return: Tuple build as (remaining amount not allocated on voucher lines, list of account_move_line created in this method)
		:rtype: tuple(float, list of int)
		'''
		if context is None:
			context = {}
		move_line_obj = self.pool.get('account.move.line')
		currency_obj = self.pool.get('res.currency')
		tax_obj = self.pool.get('account.tax')
		tot_line = line_total
		rec_lst_ids = []

		date = self.read(cr, uid, voucher_id, ['date'], context=context)['date']
		ctx = context.copy()
		ctx.update({'date': date})
		voucher = self.pool.get('account.voucher').browse(cr, uid, voucher_id, context=ctx)
		voucher_currency = voucher.journal_id.currency or voucher.company_id.currency_id
		ctx.update({
			'voucher_special_currency_rate': voucher_currency.rate * voucher.payment_rate ,
			'voucher_special_currency': voucher.payment_rate_currency_id and voucher.payment_rate_currency_id.id or False,})
		prec = self.pool.get('decimal.precision').precision_get(cr, uid, 'Account')
		for line in voucher.line_ids:
			#create one move line per voucher line where amount is not 0.0
			# AND (second part of the clause) only if the original move line was not having debit = credit = 0 (which is a legal value)
			if not line.amount and not (line.move_line_id and not float_compare(line.move_line_id.debit, line.move_line_id.credit, precision_digits=prec) and not float_compare(line.move_line_id.debit, 0.0, precision_digits=prec)):
				continue
			# convert the amount set on the voucher line into the currency of the voucher's company
			# this calls res_curreny.compute() with the right context, so that it will take either the rate on the voucher if it is relevant or will use the default behaviour
			amount = self._convert_amount(cr, uid, line.untax_amount or line.amount, voucher.id, context=ctx)
			# if the amount encoded in voucher is equal to the amount unreconciled, we need to compute the
			# currency rate difference
			if line.amount == line.amount_unreconciled:
				if not line.move_line_id:
					raise osv.except_osv(_('Wrong voucher line'),_("The invoice you are willing to pay is not valid anymore."))
				sign = voucher.type in ('payment', 'purchase') and -1 or 1
				currency_rate_difference = sign * (line.move_line_id.amount_residual - amount)
			else:
				currency_rate_difference = 0.0
			move_line = {
				'journal_id': voucher.journal_id.id,
				'period_id': voucher.period_id.id,
				'name': line.name or '/',
				'account_id': line.account_id.id,
				'move_id': move_id,
				'partner_id': voucher.partner_id.id,
				'currency_id': line.move_line_id and (company_currency <> line.move_line_id.currency_id.id and line.move_line_id.currency_id.id) or False,
				'analytic_account_id': line.account_analytic_id and line.account_analytic_id.id or False,
				'quantity': 1,
				'credit': 0.0,
				'debit': 0.0,
				'date': voucher.date
			}
			if amount < 0:
				amount = -amount
				if line.type == 'dr':
					line.type = 'cr'
				else:
					line.type = 'dr'

			if (line.type=='dr'):
				tot_line += amount
				move_line['debit'] = amount
			else:
				tot_line -= amount
				move_line['credit'] = amount

			if voucher.tax_id and voucher.type in ('sale', 'purchase'):
				move_line.update({
					'account_tax_id': voucher.tax_id.id,
				})

			if move_line.get('account_tax_id', False):
				tax_data = tax_obj.browse(cr, uid, [move_line['account_tax_id']], context=context)[0]
				if not (tax_data.base_code_id and tax_data.tax_code_id):
					raise osv.except_osv(_('No Account Base Code and Account Tax Code!'),_("You have to configure account base code and account tax code on the '%s' tax!") % (tax_data.name))

			# compute the amount in foreign currency
			foreign_currency_diff = 0.0
			amount_currency = False
			if line.move_line_id:
				# We want to set it on the account move line as soon as the original line had a foreign currency
				if line.move_line_id.currency_id and line.move_line_id.currency_id.id != company_currency:
					# we compute the amount in that foreign currency.
					if line.move_line_id.currency_id.id == current_currency:
						# if the voucher and the voucher line share the same currency, there is no computation to do
						sign = (move_line['debit'] - move_line['credit']) < 0 and -1 or 1
						amount_currency = sign * (line.amount)
					else:
						# if the rate is specified on the voucher, it will be used thanks to the special keys in the context
						# otherwise we use the rates of the system
						amount_currency = currency_obj.compute(cr, uid, company_currency, line.move_line_id.currency_id.id, move_line['debit']-move_line['credit'], context=ctx)
				if line.amount == line.amount_unreconciled:
					sign = voucher.type in ('payment', 'purchase') and -1 or 1
					foreign_currency_diff = sign * line.move_line_id.amount_residual_currency + amount_currency

			move_line['amount_currency'] = amount_currency
			voucher_line = move_line_obj.create(cr, uid, move_line)
			rec_ids = [voucher_line, line.move_line_id.id]

			if not currency_obj.is_zero(cr, uid, voucher.company_id.currency_id, currency_rate_difference):
				# Change difference entry in company currency
				exch_lines = self._get_exchange_lines(cr, uid, line, move_id, currency_rate_difference, company_currency, current_currency, context=context)
				new_id = move_line_obj.create(cr, uid, exch_lines[0],context)
				move_line_obj.create(cr, uid, exch_lines[1], context)
				rec_ids.append(new_id)

			if line.move_line_id and line.move_line_id.currency_id and not currency_obj.is_zero(cr, uid, line.move_line_id.currency_id, foreign_currency_diff):
				# Change difference entry in voucher currency
				move_line_foreign_currency = {
					'journal_id': line.voucher_id.journal_id.id,
					'period_id': line.voucher_id.period_id.id,
					'name': _('change')+': '+(line.name or '/'),
					'account_id': line.account_id.id,
					'move_id': move_id,
					'partner_id': line.voucher_id.partner_id.id,
					'currency_id': line.move_line_id.currency_id.id,
					'amount_currency': -1 * foreign_currency_diff,
					'quantity': 1,
					'credit': 0.0,
					'debit': 0.0,
					'date': line.voucher_id.date,
				}
				new_id = move_line_obj.create(cr, uid, move_line_foreign_currency, context=context)
				rec_ids.append(new_id)
			if line.move_line_id.id:
				rec_lst_ids.append(rec_ids)
		return (tot_line, rec_lst_ids)
		
	def action_move_line_create(self, cr, uid, ids, context=None):
		print "validate button"
		'''
		Confirm the vouchers given in ids and create the journal entries for each of them
		'''
		if context is None:
			context = {}
		move_pool = self.pool.get('account.move')
		move_line_pool = self.pool.get('account.move.line')
		for voucher in self.browse(cr, uid, ids, context=context):
			if voucher.move_id:
				continue
			company_currency = self._get_company_currency(cr, uid, voucher.id, context)
			current_currency = self._get_current_currency(cr, uid, voucher.id, context)
			# we select the context to use accordingly if it's a multicurrency case or not
			context = self._sel_context(cr, uid, voucher.id, context)
			# But for the operations made by _convert_amount, we always need to give the date in the context
			ctx = context.copy()
			ctx.update({'date': voucher.date})
			# Create the account move record.
			move_id = move_pool.create(cr, uid, self.account_move_get(cr, uid, voucher.id, context=context), context=context)
			# Get the name of the account_move just created
			name = move_pool.browse(cr, uid, move_id, context=context).name
			# Create the first line of the voucher
			move_line_id = move_line_pool.create(cr, uid, self.first_move_line_get(cr,uid,voucher.id, move_id, company_currency, current_currency, context), context)
			move_line_brw = move_line_pool.browse(cr, uid, move_line_id, context=context)
			
			line_total = move_line_brw.debit - move_line_brw.credit
			rec_list_ids = []
			if voucher.type == 'sale':
				line_total = line_total - self._convert_amount(cr, uid, voucher.tax_amount, voucher.id, context=ctx)
			elif voucher.type == 'purchase':
				line_total = line_total + self._convert_amount(cr, uid, voucher.tax_amount, voucher.id, context=ctx)
			# Create one move line per voucher line where amount is not 0.0
			line_total, rec_list_ids = self.voucher_move_line_create(cr, uid, voucher.id, line_total, move_id, company_currency, current_currency, context)

			# Create the writeoff line if needed
			ml_writeoff = self.writeoff_move_line_get(cr, uid, voucher.id, line_total, move_id, name, company_currency, current_currency, context)
			if ml_writeoff:
				move_line_pool.create(cr, uid, ml_writeoff, context)
			# We post the voucher.
			self.write(cr, uid, [voucher.id], {
				'move_id': move_id,
				'state': 'posted',
				'number': name,
			})
			if voucher.journal_id.entry_posted:
				move_pool.post(cr, uid, [move_id], context={})
			# We automatically reconcile the account move lines.
			reconcile = False
			for rec_ids in rec_list_ids:
				if len(rec_ids) >= 2:
					reconcile = move_line_pool.reconcile_partial(cr, uid, rec_ids, writeoff_acc_id=voucher.writeoff_acc_id.id, writeoff_period_id=voucher.period_id.id, writeoff_journal_id=voucher.journal_id.id)
		return True


	def proforma_voucher(self, cr, uid, ids, context=None):
		self.action_move_line_create(cr, uid, ids, context=context)
		return True
	
account_voucher()

class account_voucher_line1(osv.osv):
	_inherit = 'account.voucher.line'

	def resolve_o2m_operations1(cr, uid, target_osv, operations, fields, context):
		results = []
		for operation in operations:
			result = None
			if not isinstance(operation, (list, tuple)):
				result = target_osv.read(cr, uid, operation, fields, context=context)
			elif operation[0] == 0:
				# may be necessary to check if all the fields are here and get the default values?
				result = operation[2]
			elif operation[0] == 1:
				result = target_osv.read(cr, uid, operation[1], fields, context=context)
				if not result: result = {}
				result.update(operation[2])
			elif operation[0] == 4:
				result = target_osv.read(cr, uid, operation[1], fields, context=context)
			if result != None:
				results.append(result)
		return results

	def _compute_writeoff_amount1(self, cr, uid, line_dr_ids, line_cr_ids, amount, type):
		debit = credit = 0.0
		sign = type == 'payment' and -1 or 1
		for l in line_dr_ids:
			debit += l['amount1']
		for l in line_cr_ids:
			credit += l['amount1']
		return amount - sign * (credit - debit)

	def onchange_line_ids(self, cr, uid, ids, line_dr_ids, line_cr_ids, amount,total1, voucher_currency, type, context=None):
		print "writeoff_amount.........trigger"
		print "total1111111",total1
		context = context or {}
		if not line_dr_ids and not line_cr_ids:
			return {'value':{'writeoff_amount': 0.0}}
		line_osv = self.pool.get("account.voucher.line")
		print "line_osvvvvvvvv",line_osv
		line_dr_ids = resolve_o2m_operations1(cr, uid, line_osv, line_dr_ids, ['amount'], context)
		line_cr_ids = resolve_o2m_operations1(cr, uid, line_osv, line_cr_ids, ['amount'], context)
		#compute the field is_multi_currency that is used to hide/display options linked to secondary currency on the voucher
		is_multi_currency = False
		#loop on the voucher lines to see if one of these has a secondary currency. If yes, we need to see the options
		for voucher_line in line_dr_ids+line_cr_ids:
			line_id = voucher_line.get('id') and self.pool.get('account.voucher.line').browse(cr, uid, voucher_line['id'], context=context).move_line_id.id or voucher_line.get('move_line_id')
			if line_id and self.pool.get('account.move.line').browse(cr, uid, line_id, context=context).currency_id:
				is_multi_currency = True
				break
		return {'value': {'writeoff_amount1': self._compute_writeoff_amount1(cr, uid, line_dr_ids, line_cr_ids, amount, type), 'is_multi_currency': is_multi_currency}}
	

	def _compute_balance1(self, cr, uid, ids, name, args, context=None):
		currency_pool = self.pool.get('res.currency')
		rs_data = {}
		for line in self.browse(cr, uid, ids, context=context):
			ctx = context.copy()
			ctx.update({'date': line.voucher_id.date})
			voucher_rate = self.pool.get('res.currency').read(cr, uid, line.voucher_id.currency_id.id, ['rate'], context=ctx)['rate']
			ctx.update({
				'voucher_special_currency': line.voucher_id.payment_rate_currency_id and line.voucher_id.payment_rate_currency_id.id or False,
				'voucher_special_currency_rate': line.voucher_id.payment_rate * voucher_rate})
			res = {}
			company_currency = line.voucher_id.journal_id.company_id.currency_id.id
			voucher_currency = line.voucher_id.currency_id and line.voucher_id.currency_id.id or company_currency
			move_line = line.move_line_id or False
			if not move_line:
				res['amount_original'] = 0.0
				res['amount_unreconciled'] = 0.0
				res['amount_original1'] = 0.0
				res['amount_unreconciled1'] = 0.0
			elif move_line.currency_id and voucher_currency==move_line.currency_id.id:
				res['amount_original'] = abs(move_line.amount_currency)
				res['amount_unreconciled'] = abs(move_line.amount_residual_currency)
				res['amount_original1'] =  abs(move_line.amount_currency)
				res['amount_unreconciled1'] = abs(move_line.amount_residual_currency)
			else:
				#always use the amount booked in the company currency as the basis of the conversion into the voucher currency
				res['amount_original'] = currency_pool.compute(cr, uid, company_currency, voucher_currency, move_line.credit or move_line.debit or 0.0, context=ctx)
				res['amount_unreconciled'] = currency_pool.compute(cr, uid, company_currency, voucher_currency, abs(move_line.amount_residual), context=ctx)
				# res['amount_original1'] = currency_pool.compute(cr, uid, company_currency, voucher_currency, move_line.credit or move_line.debit or 0.0, context=None)
				# res['amount_unreconciled1'] = currency_pool.compute(cr, uid, company_currency, voucher_currency, abs(move_line.amount_residual), context=None)
				res['amount_original1'] = -1*move_line['amount_currency']
				res['amount_unreconciled1'] = -1*move_line['amount_currency']
				
			rs_data[line.id] = res
		return rs_data

	def onchange_amount1(self, cr, uid, ids, amount1, amount_unreconciled1, context=None):
		# print "amount idssssssss",ids

		vals = {}
		if ids:
			acc_line_obj = self.browse(cr,uid,ids)
			usd_cur = (amount1/acc_line_obj[0].voucher_id.payment_rate)
			vals['amount'] = usd_cur
			# vals['voucher_id']['total1'] = amount1
			# print acc_line_obj[0].voucher_id.id
			# self.pool.get('account.voucher').write(cr,uid,acc_line_obj[0].voucher_id.id,{'total1': amount1,'amount' :usd_cur },)
		if amount1:
			vals['reconcile'] = (amount1 == amount_unreconciled1)
		return {'value': vals}

	_columns = {
		'amount_original1' : fields.function(_compute_balance1, multi='dc', type='float', string='Original Amount', store=True, digits_compute=dp.get_precision('Account')),
		'amount_unreconciled1': fields.function(_compute_balance1, multi='dc', type='float', string='Open Balance', store=True, digits_compute=dp.get_precision('Account')),
		'reconcile' : fields.boolean('Full Reconcile'),
		'amount1':fields.float('Amount', digits_compute=dp.get_precision('Account')),
	}
	_defaults = {
		'amount1' : 0.00
			}
	def onchange_reconcile(self, cr, uid, ids, reconcile, amount, amount_unreconciled,amount_unreconciled1, context=None):
		print "idssssss",ids
		vals = {'amount': 0.0,'total1':0.0}
		print "amount_unreconciled1",amount_unreconciled1
		if reconcile:
			vals['amount'] = amount_unreconciled
			if ids:
				account_move_line_obj = self.browse(cr,uid,ids,context=None)
				vals['amount1'] = account_move_line_obj[0].amount_unreconciled1
		return {'value': vals}
account_voucher_line1()

class payment_method(osv.osv):

	_name = 'payment.new'

	_columns = {
		'payment_method' : fields.char('Payment Method',required=True),
		# 'payment_cash' : fields.char('Cash(currency)',required=True),
	}
	_rec_name = 'payment_method'
payment_method()
