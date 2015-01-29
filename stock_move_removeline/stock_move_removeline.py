import time
import pytz
from openerp import SUPERUSER_ID
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import fields, osv
from openerp import netsvc
from openerp import pooler
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.osv.orm import browse_record, browse_null
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP

class stock_move_orderline(osv.osv):

	_inherit = 'purchase.order'

	def _prepare_order_line_move(self, cr, uid, order, order_line, picking_id, context=None):
		print "hello confirm order"
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

	def _create_pickings(self, cr, uid, order, order_lines, picking_id=False, context=None):
		print "create pickings"
		"""Creates pickings and appropriate stock moves for given order lines, then
		confirms the moves, makes them available, and confirms the picking.

		If ``picking_id`` is provided, the stock moves will be added to it, otherwise
		a standard outgoing picking will be created to wrap the stock moves, as returned
		by :meth:`~._prepare_order_picking`.

		Modules that wish to customize the procurements or partition the stock moves over
		multiple stock pickings may override this method and call ``super()`` with
		different subsets of ``order_lines`` and/or preset ``picking_id`` values.

		:param browse_record order: purchase order to which the order lines belong
		:param list(browse_record) order_lines: purchase order line records for which picking
												and moves should be created.
		:param int picking_id: optional ID of a stock picking to which the created stock moves
							   will be added. A new picking will be created if omitted.
		:return: list of IDs of pickings used/created for the given order lines (usually just one)
		"""
		if not picking_id:
			picking_id = self.pool.get('stock.picking').create(cr, uid, self._prepare_order_picking(cr, uid, order, context=context))
		todo_moves = []
		stock_move = self.pool.get('stock.move')
		wf_service = netsvc.LocalService("workflow")
		for order_line in order_lines:
			if not order_line.product_id:
				continue
			if order_line.product_id.type in ('product', 'consu'):
				move = stock_move.create(cr, uid, self._prepare_order_line_move(cr, uid, order, order_line, picking_id, context=context))
				if order_line.move_dest_id and order_line.move_dest_id.state != 'done':
					order_line.move_dest_id.write({'location_id': order.location_id.id})
				todo_moves.append(move)
		print "todo list values",todo_moves
		stock_move.action_confirm(cr, uid, todo_moves)
		# stock_move.force_assign(cr, uid, todo_moves)
		# wf_service.trg_validate(uid, 'stock.picking', picking_id, 'button_confirm', cr)
		return [picking_id]

		

stock_move_orderline()
