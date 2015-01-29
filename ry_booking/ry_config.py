from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
from openerp import tools
import time
from datetime import date, timedelta

class yacht_config(osv.osv):

	def _show_bookings(self, cr, uid, ids, name, args, context=None):
		res = {}
		c_ids = self.pool.get('booking.yachts').search(cr,uid,[('yacht_id','=',ids[0])])
		for t_id in self.browse(cr,uid,ids):
			res[t_id.id] = c_ids
		return res

	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image, avoid_resize_medium=True)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

	_name='yatch.config'

	_rec_name="yatch_name"

	_order = "yatch_name desc"

	_columns = {

		# image: all image fields are base64 encoded and PIL-supported
		'image': fields.binary("Image",
			help="This field holds the image used as image for the yacht, limited to 1024x1024px."),
		'image_medium': fields.function(_get_image, fnct_inv=_set_image,
			string="Medium-sized image", type="binary", multi="_get_image",
			store={
				'yatch.config': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
			},
			help="Medium-sized image of the yacht. It is automatically "\
				 "resized as a 128x128px image, with aspect ratio preserved, "\
				 "only when the image exceeds one of those sizes. Use this field in form views or some kanban views."),
		'image_small': fields.function(_get_image, fnct_inv=_set_image,
			string="Small-sized image", type="binary", multi="_get_image",
			store={
				'yatch.config': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
			},
			help="Small-sized image of the yacht. It is automatically "\
				 "resized as a 64x64px image, with aspect ratio preserved. "\
				 "Use this field anywhere a small image is required."),
		'yatch_name' : fields.char('Yacht Name',size=100),
		'own_yatch' : fields.boolean('Own Yacht'),
		'third_yatch' : fields.boolean('Third Party'),
		'price_adult': fields.float('Price for Adult'),
		'price_children': fields.float('Price for Children'),
		'charges_id' : fields.one2many('yacht.charges.line','y_id','Yacht Charges'),
		'price_charge': fields.float('Price'),
		'desc':fields.text('Description'),
		'party_name':fields.char('Third Party Name'),
		'booking_ids': fields.function(_show_bookings, relation='booking.yachts', type="many2many", string='Bookings'),
		'max_no_pass': fields.integer('Max No of Passengers'),
		'length' : fields.char('Length'),
		'license_no' : fields.char('License No'),
		'cap_name' : fields.many2one('hr.employee','Captain Name',domain="[('yacht_name','=',yatch_name)]"),
		'cap_no': fields.char('Captain Number'),
		'cap_email' : fields.char('Captain Email'),
		'no_crew_board' : fields.integer('Number of Crew on Board'),
		'park_loc':fields.char('Parking Location'),
		'park_no' : fields.char('Parking Number'),
		'manfac_year' : fields.date('Manufacturing Year'),
		'ser_time_prd' : fields.integer('Service time period(in hours)'),
		'min_dep' : fields.float('Min Deposit'),
		# 'last_ser_date' : fields.date('Last Service Date'),
		# 'ser_in_days' : fields.char('Serviced (in Days)'),
		# 'next_ser_time' : fields.date('Next Service Date'),
		# 'services_id' : fields.one2many('yacht.services','servive_id','Service History'),
}

	def onchange_next_service(self,cr,uid,ids,last_ser_date,ser_in_days,context=None):
		if not last_ser_date:
			raise osv.except_osv(_('Last Serivce Date is not selected !'),
							_('Please Select a Service Date 1st.'))
		res={}
		dt = datetime.datetime.strptime(last_ser_date, "%Y-%m-%d")
		d=dt+timedelta(days=int(ser_in_days))
		res.update({'next_ser_time':str(d)})
		return {'value':res}

	

	def service_day_checking(self, cr, uid, context=None):
		yatch_ids = self.pool.get('yatch.config').search(cr,uid,[('id','!=',False)])
		for x in yatch_ids:
			obj = self.pool.get('yatch.config').browse(cr,uid,x)
			if obj.next_ser_time:
				next_ser_date = obj.next_ser_time
				dt = datetime.datetime.strptime(next_ser_date, "%Y-%m-%d")
				today =  datetime.datetime.now()
				diff = today - dt
				if diff.days == 1:
					up_date = dt + datetime.timedelta(days=int(obj.ser_in_days))
					self.pool.get('yatch.config').write(cr,uid,x,{'services_id': [[0, False, {'next_ser_time':obj.next_ser_time , 'state': 'left', 'yacht_id': x,'last_ser_date':obj.last_ser_date}]]})
					self.pool.get('yatch.config').write(cr,uid,x,{'last_ser_date' : obj.next_ser_time,'next_ser_time' : str(up_date).split()[0]})
		return True

	def onchange_type(self,cr,uid,ids,own_yatch,third_yatch,context=None):
		res={}
		if own_yatch==True:
			res.update({'third_yatch':False})
		return {'value':res}

	def onchange_type1(self,cr,uid,ids,own_yatch,third_yatch,context=None):
		res={}
		if third_yatch==True:
			res.update({'own_yatch':False})
		return {'value':res}

	def onchange_emp(self,cr,uid,ids,cap_name,context=None):
		res = {}
		emp_obj = self.pool.get('hr.employee').browse(cr,uid,cap_name)
		if emp_obj:
			res.update({'cap_no':emp_obj.work_phone,'cap_email':emp_obj.work_email})
		return {'value':res}
yacht_config()

class yacht_charges_line(osv.osv):
	_name = 'yacht.charges.line'
	_columns = {
		'y_id' : fields.many2one('yatch.config','Yacht id'),
		# 'charge_name' : fields.char('Charge Name'),
		'price_charge': fields.float('Price'),
		'charge_id' : fields.many2one('yacht.charges','Charge'),
		'charge_type':fields.selection([('hour', 'Per Hour'), ('day', 'Per Day'),('week', 'Per Week')], 'Charge For'),
		}

	def onchange_charge(self,cr,uid,ids,charge_id,context=None):
		res={'value':{}}
		ch_obj = self.pool.get('yacht.charges').browse(cr,uid,charge_id)
		res['value'].update({'price_charge':ch_obj.price_charge,'charge_type':ch_obj.charge_type})
		return res


yacht_charges_line()

class yacht_charges(osv.osv):
	_name = 'yacht.charges'

	_rec_name="charge_name"

	_columns = {
		'charge_name' : fields.char('Charge Name'),
		'price_charge': fields.float('Price'),
		'charge_type':fields.selection([('hour', 'Per Hour'), ('day', 'Per Day'),('week', 'Per Week')], 'Charge For'),
		}

yacht_charges()

class service_yacht(osv.osv):

	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
		default.update({
			'name': self.pool.get('ir.sequence').get(cr, uid, 'yacht.services'),
			'state':'left',
		})
		return super(service_yacht, self).copy(cr, uid, id, default, context=context)

	_name='yacht.services'
	_columns = {
		'servive_id' : fields.many2one('yatch.config'),
		'yacht_id' : fields.many2one('yatch.config','Yacht Name'),
		'sequence' : fields.char('ServiceID'),
		'last_ser_date' : fields.date('Last Service Date'),
		'next_ser_time' : fields.date('Next Service Date'),
		"state" : fields.selection([('left','Left'),('done','Done')],'State'),
	}

	_defaults = {
		# 'sequence' : _get_code,
		'state':'left',
	}

	def service_status_change(self, cr, uid,ids,context=None):
		write=self.write(cr,uid,ids,{'state' : 'done'},context=None)
		return True

	def services_dates(self,cr,uid,ids,yacht_id,context=None):
		res={}
		yacht_obj = self.pool.get('yatch.config').browse(cr,uid,yacht_id)
		if yacht_obj:
			res.update({'last_ser_date':yacht_obj.last_ser_date,'next_ser_time':yacht_obj.next_ser_time})
		return {'value':res}

	def create(self, cr, uid, vals, context=None):
		if vals.get('sequence','/')== '/':
			vals['sequence'] = self.pool.get('ir.sequence').get(cr, uid, 'yacht.services') or '/'
		return super(service_yacht, self).create(cr, uid, vals, context=context)

service_yacht()

class captain_configuration(osv.osv):

	_inherit="hr.employee"

	_columns={
	'yacht_name':fields.char('Yacht Name'),
	'parent_id': fields.many2one('hr.employee', 'Manager',required=True),
	'work_email': fields.char('Work Email', size=240,required=True),
	}

captain_configuration()

class hr_job_inherit(osv.osv):

	_inherit="hr.job"

hr_job_inherit()