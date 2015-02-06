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
		'cst_ref' : fields.char("Cst Ref"),
		'cst':fields.char('Product/work'),
		'work_order_id':fields.many2one('work.order','Work Order'),
		'ref':fields.char('REF'),
		'color':fields.char('Color'),
		'gauge':fields.char('Gauge'),
		'date':fields.datetime('Date'),
		'width':fields.char('Width'),
		'manufacture_date':fields.date('MFG'),
		'expiry_date':fields.date('Exp'),
		# 'roll_no':fields.char('Jumbo Roll No.'),
		'jumbo_roll' : fields.many2one('jumbo.roll','Jumbo roll No'),
		'seq' : fields.char('Seq'),
		'gross_weight':fields.char('Gross Weight'),
		'tr_weight':fields.float('Tare Weight'),
		'net_weight':fields.float('Net Weight'),
		'pallet_no':fields.integer('Pallet No.'),
		'for_sample':fields.boolean('For Sample??'),
		'field_label_id' : fields.many2one('label.printing.field','Field Id'),
		'country_origin' : fields.char('Country Of origin'),
		'img' : fields.binary('Logo'),
		'active': fields.boolean('Active', help="If unchecked, it will allow you to hide the Packaging record without removing it."),
	}

	_defaults = {
		'active': 1,
		'date' :  fields.datetime.now
	}
	_rec_name = 'field_label_id'
	_order = "date desc"
	def create(self, cr, uid, vals, context=None):
		print "work orderweeeeeeeeeeeee"
		if vals['gauge']:
			guage = vals['gauge']
			vals.update({'gauge':guage + 'u' })
		if vals['width']:
			width = vals['width']
			vals.update({'width' : width + 'mm'})
		if vals['tr_weight']:
			tr_wgt = vals['tr_weight']
			vals.update({'tr_weight' : tr_wgt })
		if vals['tr_weight']:
			net_wgt = vals['net_weight']
			vals.update({'net_weight' : net_wgt })
		if vals['gross_weight']:
			gross_weight = vals['gross_weight']
			vals.update({'gross_weight': str(gross_weight) + 'Kg' })
		customer = self.pool.get('res.partner').browse(cr,uid,vals['customer'])
		if customer:
			cst_ref = vals['cst'] + ' ' + customer.name
			vals.update({'cst_ref' : cst_ref})
		if vals['for_sample']==True:
			vals.update({'active':False})
		# if vals.get('name','/')== '/':
		# 	vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'packaging.board') or '/'
		return super(packaging_board, self).create(cr, uid, vals, context=context)

	def write(self,cr,uid,ids,vals,context=None):
		# print vals['cst']
		# print vals['customer']
		if 'for_sample' in vals:
			if vals['for_sample']==True:
				vals.update({'active':False})
		return super(packaging_board, self).write(cr, uid, ids, vals, context=context)

	def onchange_weight(self,cr,uid,ids,tr_weight,net_weight,context=None):
		print tr_weight
		print net_weight
		res={}
		res.update({'gross_weight':tr_weight+net_weight})
		return {'value':res}

	def onchange_customer(self,cr,uid,ids,customer,context=None):
		print "hellloo its is customerrrrrrrrrrrrrrrrrrrrrrrrrrr"
		res={}
		cust_obj = self.pool.get('res.partner').browse(cr,uid,customer)
		print "image",cust_obj.image
		res.update({'ref':cust_obj.reference})
		w_id = self.pool.get('work.order').search(cr,uid,[('customer_id','=',customer)])
		if w_id:
			w_obj = self.pool.get('work.order').browse(cr,uid,w_id[0])
			# label_id = self.pool.get('label.printing.field').search(cr,uid,[('label_id','=',w_id[0])])
			# if label_id:
			# 	pkg_obj = self.pool.get('label.printing.field').browse(cr,uid,label_id[0],context=None)
			res.update({'work_order_id' : w_id[0],
				'gauge':str(w_obj.gauge),
				'net_weight':w_obj.net_weight,
				'color':w_obj.color,
				# 'roll_no' : wr_obj.roll_no,
				# 'date':w_obj.date,
				'cst':w_obj.work_order,
				'width':str(w_obj.width),
				'tr_weight':w_obj.tare_weight,
				'ref' : cust_obj.name,
				'country_origin' : w_obj.country_origin,
				'expiry_date': w_obj.expiry_date,
				# 'field_label_id':pkg_obj.id,
				'manufacture_date' :w_obj.date,
				'img' : cust_obj.image,
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
				'gauge':str(wr_obj.gauge),
				'net_weight':wr_obj.net_weight,
				'color':wr_obj.color,
				# 'roll_no' : wr_obj.roll_no,
				# 'date':wr_obj.date,
				'cst':wr_obj.work_order,
				'width':str(wr_obj.width),
				'tr_weight':wr_obj.tare_weight,
				'ref':cust_obj.name,
				'expiry_date': wr_obj.expiry_date,
				'manufacture_date' :wr_obj.date,
				'country_origin' : wr_obj.country_origin,
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

	def onchange_jumboroll(self,cr,uid,ids,jumbo_roll,context= None):
		print "hello000000000000000000000000000000000000000000000000"
		res={}
		jumbo_id = self.pool.get('packaging.board').search(cr,uid,[('jumbo_roll','=',jumbo_roll)])
		jumbo_id_count = len(jumbo_id) + 1
		res.update({'seq' :('0'+str(jumbo_id_count)) })
		return {'value':res}


	def print_report(self, cr, uid, ids, context=None):
		for i in range(0,5):
			print "hello000000000000000"
			'''
			This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
			'''
			assert len(ids) == 1, 'This option should only be used for a single id at a time'
			datas = {
					'model': 'packaging.board',
					'ids': ids,
					'form': self.read(cr, uid, ids[0], context=context),
				}
			return {'type': 'ir.actions.report.xml', 'report_name': 'packaging.board', 'datas': datas, 'nodestroy': True}

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
	'color':fields.char('Color'),
	'gauge':fields.integer('Gauge'),
	'width':fields.integer('Width'),
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
	'country_origin' : fields.char('Country Of origin'),
	}
	_defaults = {
		'shift' : 'day',
		'date' : str(date.today()),
		'year_in_num' : 2,
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
		'color_code' : fields.many2one('color.code','Color Code'),
		'color' : fields.many2one('color.name','Color'),
		'gauge' : fields.integer('Gauge'),
		'width' : fields.integer('Slit Roll Width'),
		'jumbo_up': fields.char('Up'),
		'jumbo_width':fields.char('Jumbo Width'),
		'core_id' : fields.char('CoreId'),
		'od' : fields.char('OD'),
		'wt' : fields.char('Wt'),
		'length' : fields.char('Length'),
		# 'stamp_no' : fields.char('Stamp No',required=True),
	}
workorder_items()

class color_code123(osv.osv):
	_name = 'color.code'
	_columns = {
		'color_code' : fields.char('Color Code',required=True),
	}
	_rec_name = 'color_code'
color_code123()

class color_name(osv.osv):
	_name = 'color.name'
	_columns = {
		'color_name' : fields.char('Color',required=True) 
	}
	_rec_name = 'color_name'
color_name()

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

class jumbo_roll(osv.osv):

	def serial_123(self,cr,uid,ids,field_name, arg, context=None):
		res={}
		counter=0
		for i in self.browse(cr,uid,ids,context=None):
			res[i.id]={
					'sl_no':01
				}
			counter+=1
			res[i.id]['sl_no'] = counter
		return res

	_name = 'jumbo.roll'
	_columns = {
		'jumbo_roll' : fields.char('Jumbo Roll No',required=True),
		'sl_no':fields.function(serial_123,string='Sl.No',type="integer",multi="sums"),
	}
	_rec_name = 'jumbo_roll'

	# def onchange_jumboroll(self,cr,uid,ids,jumbo_roll,context= None):
	# 	res={}
	# 	print  jumbo_roll
	# 	return {'value':res}
jumbo_roll()