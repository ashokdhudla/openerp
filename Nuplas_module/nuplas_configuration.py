from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import time
from dateutil.relativedelta import relativedelta
from datetime import timedelta
class customer_setup(osv.osv):

	_inherit="res.partner"

	_columns={
	'reference':fields.char('Reference'),
	}
	
customer_setup()

class product_setup(osv.osv):

	_inherit="product.product"

product_setup()

class packaging_board(osv.osv):

	_name = 'packaging.board'

	def serial_inc(self,cr,uid,ids,field_name, arg, context=None):
		res={}
		counter=0
		for i in self.browse(cr,uid,ids,context=None):
			res[i.id]={
					'sl_no':1
				}
			counter+=1
			res[i.id]['sl_no'] = counter
		return res

	# def copy(self, cr, uid, id, default=None, context=None):
	# 	if not default:
	# 		default = {}
	# 	default.update({
 #            'name': self.pool.get('ir.sequence').get(cr, uid, 'packaging.board'),
 #        })
	# 	return super(packaging_board, self).copy(cr, uid, id, default, context=context)

	_columns = {
		# 'name':fields.char("Packaging ID",size=200,readonly=True),
		'sl_no':fields.function(serial_inc,string='Sl.No',type="integer",multi="sums" ,readonly=True),
		'customer':fields.many2one('res.partner',"Customer",domain="[('customer','=',True)]"),
		'product':fields.many2one('product.product',"Product"),
		'cst':fields.char('Work Order'),
		'work_order_id':fields.many2one('work.order','Work Order'),
		'ref':fields.char('REF'),
		'color':fields.char('Color'),
		'color1' : fields.boolean('Color1'),
		'gauge':fields.float('Gauge'),
		'date':fields.datetime('Date'),
		'width':fields.float('Width'),
		'manufacture_date':fields.date('MFG'),
		'expiry_date':fields.date('Exp'),
		'roll_no':fields.char('Jumbo Roll No.'),
		'gross_weight':fields.float('Gross Weight'),
		'tr_weight':fields.float('Tare Weight'),
		'net_weight':fields.float('Net Weight'),
		#'size':fields.integer('Size'),
		'pallet_no':fields.integer('Pallet No.'),
		'for_sample':fields.boolean('For Sample??'),
		'field_label_id' : fields.many2one('label.printing.field','Field Id'),
		'active': fields.boolean('Active', help="If unchecked, it will allow you to hide the Packaging record without removing it."),
	}

	_defaults = {
		'active': 1,
		'date' :  fields.datetime.now
	}
	_rec_name = 'field_label_id'
	_order = "date desc"
	def create(self, cr, uid, vals, context=None):

		if vals['for_sample']==True:
			vals.update({'active':False})
		# if vals.get('name','/')== '/':
		# 	vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'packaging.board') or '/'
		return super(packaging_board, self).create(cr, uid, vals, context=context)

	def write(self,cr,uid,ids,vals,context=None):
		print vals
		if 'for_sample' in vals:
			if vals['for_sample']==True:
				vals.update({'active':False})
		return super(packaging_board, self).write(cr, uid, ids, vals, context=context)

	def onchange_weight(self,cr,uid,ids,tr_weight,net_weight,context=None):
		res={}
		res.update({'gross_weight':tr_weight+net_weight})
		return {'value':res}

	def onchange_customer(self,cr,uid,ids,customer,context=None):
		res={}
		cust_obj = self.pool.get('res.partner').browse(cr,uid,customer)
		res.update({'ref':cust_obj.reference})
		w_id = self.pool.get('work.order').search(cr,uid,[('customer_id','=',customer)])
		if w_id:
			w_obj = self.pool.get('work.order').browse(cr,uid,w_id[0])
			# label_id = self.pool.get('label.printing.field').search(cr,uid,[('label_id','=',w_id[0])])
			# if label_id:
			# 	pkg_obj = self.pool.get('label.printing.field').browse(cr,uid,label_id[0],context=None)
			res.update({'work_order_id' : w_id[0],
				'gauge':w_obj.gauge,
				'net_weight':w_obj.net_weight,
				'color':w_obj.color,
				# 'roll_no' : wr_obj.roll_no,
				# 'date':w_obj.date,
				'cst':w_obj.work_order,
				'width':w_obj.width,
				'tr_weight':w_obj.tare_weight,
				'ref' : cust_obj.name,
				'expiry_date': w_obj.expiry_date,
				# 'field_label_id':pkg_obj.id,
				'manufacture_date' :w_obj.date
				})
			return {'value':res}
		else:
			res.update({
					'gauge':'',
					'net_weight':'',
					'color':'',
					'date':'',
					'cst':'',
					})
		return {'value':res}

	def onchange_workorder(self,cr,uid,ids,cst,context=None):
		print "onchange is hitiing the values"
		res={}
		wr_id = self.pool.get('work.order').search(cr,uid,[('work_order','=',cst)])
		if wr_id:
			wr_obj = self.pool.get('work.order').browse(cr,uid,wr_id[0])
			cust_obj = self.pool.get('res.partner').browse(cr,uid,wr_obj.customer_id.id,context=None)
			res.update({'customer':wr_obj.customer_id.id,
				'gauge':wr_obj.gauge,
				'net_weight':wr_obj.net_weight,
				'color':wr_obj.color,
				'roll_no' : wr_obj.roll_no,
				# 'date':wr_obj.date,
				'cst':wr_obj.work_order,
				'width':wr_obj.width,
				'tr_weight':wr_obj.tare_weight,
				'ref':cust_obj.name,
				'expiry_date': wr_obj.expiry_date,
				'manufacture_date' :wr_obj.date,
				'work_order_id' : wr_id[0]
				})
			return {'value':res}
		else:
			res.update({
					'gauge':'',
					'net_weight':'',
					'color':'',
					'date':'',
					'cst':'',
					})
		return {'value':res}


		

packaging_board()


class work_order(osv.osv):

	_name = 'work.order'

	def _get_packagings(self, cr, uid, ids, name, args, context=None):
		res = {}
		cntr_obj=self.browse(cr,uid,ids)
		for i in cntr_obj:
			pkg_ids = self.pool.get('packaging.board').search(cr,uid,[('customer','=',i.customer_id.id),('cst','=',i.work_order)])
			res[i.id] = pkg_ids
		return res

	_columns={
	'customer_id':fields.many2one('res.partner','Customer',domain="[('customer','=',True)]"),
	# 'product_id' : fields.many2one('product.product','Product',domain ="[('product','=',True]"),
	# 'mother_roll_no':fields.char('Jumbo Roll No.'),
	'color':fields.char('Color'),
	'gauge':fields.float('Gauge'),
	'width':fields.float('Width'),
	'net_weight':fields.float('Net Weight'),
	'tare_weight':fields.float('Tare Weight'),
	'meters':fields.float('Meters'),
	'date':fields.date('Date'),
	'shift':fields.selection([('day', 'Day'), ('night', 'Night')], 'Shift'),
	'work_order':fields.char('Work Order'),
	'year_in_num':fields.integer("Expiry Year in number"),
	'expiry_date':fields.date("Expiry Date"),
	'field_ids' : fields.one2many("label.printing.field", 'label_id', 'Fields'),
	'packaging_ids':fields.function(_get_packagings, relation='packaging.board', type="many2many", string='Packagings',readonly=True),
	'color_ftp':fields.boolean('Color'),
	'gauge_ftp':fields.boolean('Gauge'),
	'width_ftp':fields.boolean('Width'),
	'net_weight_ftp':fields.boolean('Net Weight'),
	'shift_ftp':fields.boolean('Shift'),
	'expiry_date_ftp':fields.boolean("Expiry Date"),
	'no_copies' : fields.char('No Of Copies'),
	'label_height' : fields.char('Height',palceholder="ex:9.0"),
	'label_width' : fields.char('Width',palceholder="ex:4.0"),
	'items_id' : fields.one2many('workorder.items','wo_items'),
	'order_no' : fields.char('Order NO'),
	'application': fields.char('Application'),
	'roll_no' : fields.char('Roll No'),
	}
	_defaults = {
		'shift' : 'day',
		'date' : str(date.today())
	}

	# _sql_constraints = [('work_order','unique(work_order)', 'Work Order already exists...!')]

	# def create(self,)
	def onchange_expiry(self,cr,uid,ids,year_in_num,context= None):
		res={}
		today = date.today()
		ex_date = str(today+relativedelta(years=+year_in_num))
		res.update({'expiry_date':ex_date})
		return {'value':res}
		
work_order()


class workorder_items(osv.osv):
	_name = 'workorder.items'
	_description = "work order information"

	def serial_inc1(self,cr,uid,ids,field_name, arg, context=None):
		res={}
		counter=0
		for i in self.browse(cr,uid,ids,context=None):
			res[i.id]={
					'sl_no':1
				}
			counter+=1
			res[i.id]['sl_no'] = counter
		return res
	_columns= {
		'wo_items' : fields.many2one('work.order'),
		'sl_no':fields.function(serial_inc1,string='Sl.No',type="integer",multi="sums" ,readonly=True),
		'color_code' : fields.char('Color Code',required=True),
		'color' : fields.char('Color'),
		'gauge' : fields.char('Gauge'),
		'width' : fields.char('Slit Roll Width'),
		'jumbo_up': fields.char('Up'),
		'jumbo_width':fields.char('Jumbo Width'),
		'core_id' : fields.char('CoreId'),
		'od' : fields.char('OD'),
		'wt' : fields.char('Wt'),
		'length' : fields.char('Length'),
		# 'stamp_no' : fields.char('Stamp No',required=True),
	}
workorder_items()

class label_printing(osv.osv):

	_name="label.printing.field"

	_columns={
	'sequence' : fields.integer("Sequence", required=True),
	'label_id':fields.many2one('work.order','Work Order'),
	'field_id' : fields.many2one('ir.model.fields', 'Fields',domain="[('model','=','work.order')]"),
	}

	def create(self,cr,uid,vals,context=None):
		# print "create method vals",vals['label_id']
		# wrk_id = self.search(cr,uid,vals['label_id'],context=None)
		# print wrk_id
		print vals
		wrk_obj = self.browse(cr,uid,vals['label_id'],context=None)
		# if wrk_obj:
			# print wrk_obj.field_id.name
			# print wrk_obj.field_id
		pkg_obj = self.pool.get('packaging.board').browse(cr,uid,vals['label_id'],context=None)
		print pkg_obj
		return super(label_printing,self).create(cr,uid,vals,context=None)
	# def write(self,cr,uid,vals,context=None):
	# 	print "write method vals",vals
	# 	return super(label_printing,self).write(cr,uid,vals,context=None)

label_printing()