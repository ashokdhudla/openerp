
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import openerp.addons.decimal_precision as dp
from openerp import netsvc
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import datetime
import re

class customer_setup(osv.osv):

	_inherit="res.partner"
	
customer_setup()

class booking_person(osv.osv):

	_inherit="res.users"

booking_person()

class booking_yachts(osv.osv):

	_name = 'booking.yachts'

	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
		default.update({
			'name': self.pool.get('ir.sequence').get(cr, uid, 'booking.yachts'),
			'state':'draft',
		})
		return super(booking_yachts, self).copy(cr, uid, id, default, context=context)

	_columns = {
		'name':fields.char("Booking ID",size=200,readonly=True),
		'book_for':fields.selection([('hour', 'Hour'), ('day', 'Day'),('week', 'Week')], 'Book For'),
		'yacht_id':fields.many2one('yatch.config','Yacht Name'),
		# 'yacht_line':fields.one2many('booking.yachts.line','yacht_line_id','Booking Line'),

		'client_id':fields.many2one('res.partner','Name of the Client',domain="[('customer','=',True)]",required=True),
		'contact_num':fields.char('Contact Number'),
		'no_guests':fields.integer('No. of Guests'),
		'cruise_date':fields.date('Date of Cruise',required=True),
		'mail':fields.char('Email',size=120,required=True),
		'time1':fields.integer('Time'),
		'time2':fields.integer('Time'),
		'am_pm':fields.selection([('am', 'AM'), ('pm', 'PM')], "AM/PM"),
		'am_pm1':fields.selection([('am', 'AM'), ('pm', 'PM')], "AM/PM"),
		'total_hrs':fields.integer('Total Hours Cruising'),
		'cost_per_hr':fields.float('Cost Per Hour/Day/Week'),
		'amount_total':fields.float('Total Amount'),
		# 'half_amt_received':fields.selection([('yes', 'Yes'), ('no', 'No')], "50%  Deposit Received"),
		'half_amt_received':fields.boolean("50%  Deposit Received"),
		'amount_received':fields.float('Amount Received'),
		'amt_date':fields.date('Amount Received On'),
		'amt_bal':fields.float('The Amount Need to be Collected before departing'),
		# 'catering':fields.selection([('yes', 'Yes'), ('no', 'No')], "Catering"),
		'catering':fields.boolean('Catering'),
		# 'catering_n':fields.boolean('No'),
		'cat_company':fields.char('Catering Company'),
		'contact_point':fields.char('Contact Point'),
		# 'own_food':fields.selection([('yes', 'Yes'), ('no', 'No')], "Own food"),
		'own_food':fields.boolean( "Own food"),
		'food_type':fields.char('Type of food'),
		'food_pax':fields.char('Food Pax'),
		# 'catering_board':fields.selection([('yes', 'Yes'), ('no', 'No')], "Catering With Crew on Board"),
		'catering_board':fields.boolean("Catering With Crew on Board"),
		'no_on_board':fields.integer('How Many on Board'),
		# 'decoration':fields.selection([('yes', 'Yes'), ('no', 'No')], "Decoration"),
		'decoration':fields.boolean("Decoration"),
		'occasion_type':fields.char('Type of Occasion'),
		# 'dj':fields.selection([('yes', 'Yes'), ('no', 'No')], "DJ"),
		'dj':fields.boolean("DJ"),
		'contact_num2':fields.char('Contact Number'),
		'remarks':fields.text('Outline or Remarks'),
		# 'sales_remarks' : fields.text(' Charter Sales and Remarks'),
		# 'luxury_transportation' : fields.selection([('yes','Yes'),('no','No')],'Luxury_Transportation'),
		'luxury_transportation' : fields.boolean('Luxury Transportation'),
		'contact_no_chauffeur' : fields.char('Contact No of Chauffeur'),
		# 'water_sports':fields.selection([('yes','Yes'),('no','No')],'Water Sports'),
		'water_sports':fields.boolean('Water Sports'),
		'supplier_contact_point': fields.char('Supplier Contact Point'),
		'time_for_sport_activity':fields.char('Time of Water Sport Activity'),
		'type_water_sports' : fields.char('Type of Water Sports'),
		# 'client_bring_alcohol' : fields.selection([('yes','Yes'),('no','No')],'Client Will Bring Alcohol'),
		'client_bring_alcohol' : fields.boolean('Client Will Bring Alcohol'),
		'need_to_prepare':fields.char('Need To Prepare'),
		'client_activity_remarks':fields.text('Client Activity Remarks'),
		'charter_sales_remarks' : fields.text('Charter Sales Remarks'),
		'booked_by':fields.many2one('res.users','Booked by'),
		'signature': fields.text('Signature'),
		'phone':fields.char('Contact Number'),
		'src':fields.selection([('internet','Internet'),('phone','Phone'),('add','Addvertisement'),('word','Word Of Mouth'),('google','Google Adds'),('social media','Social Media'),('sales team','Sales Team'),('others','Others')],'Source Of Booking'),
		'state':fields.selection([('draft','Draft'),
			('approved','Approved'),
			('quotation','Quotation'),
			('done','Done'),
			('cancel','Cancelled')],'Status'),
		'security_deposit':fields.char('Security Deposit',readonly=True),
	}

	_defaults={
	'no_guests':1,
	'state':'draft',
	'security_deposit':'10%',
	}

	_order = "name desc"


	def create(self, cr, uid, vals, context=None):
		if vals.get('name','/')== '/':
			vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'booking.yachts') or '/'
		t_hrs = vals['time1']-vals['time2']
		if t_hrs < 0:
			t_hrs = (t_hrs)*(-1)
		vals['total_hrs'] = t_hrs
		yacht_ids = vals['yacht_id']	
		yacht_obj = self.pool.get('yacht.charges').browse(cr,uid,yacht_ids)
		cruise_date = datetime.datetime.strptime(vals['cruise_date'], "%Y-%m-%d")
		print "create method"
		print "yacht_obj.charge_name",yacht_obj.charge_name
		print cruise_date.weekday()
		if yacht_obj.charge_name == "Weekend":
				if cruise_date.weekday() == 5 or cruise_date.weekday() == 4:
					print "weekends"
					vals['cost_per_hr'] = yacht_obj.price_charge
					addamt= yacht_obj.price_charge*t_hrs*0.1
					amount = yacht_obj.price_charge*t_hrs+addamt
					vals['amount_total'] = yacht_obj.price_charge*t_hrs+addamt
		if yacht_obj.charge_name == "Weekday":
				if cruise_date.weekday() == 0 or cruise_date.weekday() == 1 or cruise_date.weekday() == 2 or cruise_date.weekday() == 3 or cruise_date.weekday() == 6:
					vals['cost_per_hr'] = yacht_obj.price_charge
					print "weekdaysss"
					addamt= yacht_obj.price_charge*t_hrs*0.1
					amount = yacht_obj.price_charge*t_hrs+addamt
					vals['amount_total'] = yacht_obj.price_charge*t_hrs+addamt
		booking_id = super(booking_yachts, self).create(cr, uid, vals, context=context)
		email_list=[]
		booking_obj = self.pool.get('booking.yachts').browse(cr,uid,booking_id)
		cust_obj = self.pool.get('res.partner').browse(cr,uid,booking_obj.client_id.id)
		yacht_obj = self.pool.get('yatch.config').browse(cr,uid,booking_obj.yacht_id.id)
		if (booking_obj.total_hrs == yacht_obj.ser_time_prd):
			m_ids = self.pool.get('ir.mail_server').search(cr,uid,[('active','=','True')])
			mail_obj = self.pool.get('ir.mail_server').browse(cr,uid,m_ids[0],context)
			email_list.append(yacht_obj.cap_email)
			email_list.append(yacht_obj.cap_name.parent_id.work_email)
			username =mail_obj.smtp_user
			password =mail_obj.smtp_pass
			host = mail_obj.smtp_host
			port = mail_obj.smtp_port
			fromaddr = username
			server = smtplib.SMTP(host+':'+'587')
			server.ehlo()
			server.starttls()
			server.ehlo()
			server.login(username, password)
			msg = MIMEMultipart()
			msg['From'] = fromaddr
			msg['Subject'] = 'Royal Yachts Booking Information'
			toaddr = email_list 
			msg['To'] =", ".join(email_list)
			text = text = ('<p><h2>Hello Sir/Madam,</h2></p><p><b>%s is need to be serviced as per its service time is %s:00 hours</b></p>')%(yacht_obj.yatch_name,yacht_obj.ser_time_prd)
			body = MIMEText(text, _subtype='html')
			msg.attach(body)
			server.sendmail(fromaddr, email_list, msg.as_string())
			server.quit()
		return booking_id

	def write(self,cr,uid,ids,vals,context=None):
		booking_obj = self.pool.get('booking.yachts').browse(cr,uid,ids)
		
		if 'cruise_date'in vals:
			cruise_date = datetime.datetime.strptime(vals['cruise_date'], "%Y-%m-%d")
		else:
			cruise_date = datetime.datetime.strptime(booking_obj[0].cruise_date, "%Y-%m-%d")
		print "write method"
		if 'time1' in vals:
			if 'time2' in vals:
				t_hrs = vals['time1']-vals['time2']
			else:
				t_hrs = vals['time1']-booking_obj[0].time2
			if t_hrs < 0:
				t_hrs = (t_hrs)*(-1)
			vals['total_hrs'] = t_hrs
			yacht_obj = self.pool.get('yacht.charges').browse(cr,uid,booking_obj[0].yacht_id.id)
			if yacht_obj.charge_name == "Weekend":
				if cruise_date.weekday() == 5 or cruise_date.weekday() == 4:
					vals['cost_per_hr'] = yacht_obj.price_charge
					addamt= yacht_obj.price_charge*t_hrs*0.1
					amount = yacht_obj.price_charge*t_hrs+addamt
					vals['amount_total'] = yacht_obj.price_charge*t_hrs+addamt
					print "time1 change"
			if yacht_obj.charge_name == "Weekday":
				if cruise_date.weekday() == 0 or cruise_date.weekday() == 1 or cruise_date.weekday() == 2 or cruise_date.weekday() == 3 or cruise_date.weekday() == 6:
					vals['cost_per_hr'] = yacht_obj.price_charge
					addamt= yacht_obj.price_charge*t_hrs*0.1
					amount = yacht_obj.price_charge*t_hrs+addamt
					vals['amount_total'] = yacht_obj.price_charge*t_hrs+addamt
					print "time1 change"
		if 'time2' in vals:
			if 'time1' in vals:
				t_hrs = vals['time1']-vals['time2']
			else:
				t_hrs = booking_obj[0].time1-vals['time2']
			if t_hrs < 0:
				t_hrs = (t_hrs)*(-1)
			vals['total_hrs'] = t_hrs
			yacht_obj = self.pool.get('yacht.charges').browse(cr,uid,booking_obj[0].yacht_id.id)
			if yacht_obj.charge_name == "Weekend":
				if cruise_date.weekday() == 5 or cruise_date.weekday() == 4:
					vals['cost_per_hr'] = yacht_obj.price_charge
					addamt= yacht_obj.price_charge*t_hrs*0.1
					amount = yacht_obj.price_charge*t_hrs+addamt
					vals['amount_total'] = yacht_obj.price_charge*t_hrs+addamt
					print "time2 change"
			if yacht_obj.charge_name == "Weekday":
				if cruise_date.weekday() == 0 or cruise_date.weekday() == 1 or cruise_date.weekday() == 2 or cruise_date.weekday() == 3 or cruise_date.weekday() == 6:
					vals['cost_per_hr'] = yacht_obj.price_charge
					addamt= yacht_obj.price_charge*t_hrs*0.1
					amount = yacht_obj.price_charge*t_hrs+addamt
					vals['amount_total'] = yacht_obj.price_charge*t_hrs+addamt
					print "time2 change"
			
		# print vals['time1']
		# t_hrs = vals['time1']-vals['time2']
		# if t_hrs < 0:
		# 	t_hrs = (t_hrs)*(-1)
		# vals['total_hrs'] = t_hrs
		# yacht_ids = vals['yacht_id']	
		# yacht_obj = self.pool.get('yacht.charges').browse(cr,uid,yacht_ids)
		# cruise_date = datetime.datetime.strptime(vals['cruise_date'], "%Y-%m-%d")
		# if yacht_obj.charge_name == "Weekend":
		# 		if cruise_date.weekday() == 5 or cruise_date.weekday() == 4:
		# 			vals['cost_per_hr'] = yacht_obj.price_charge
		# 			addamt= yacht_obj.price_charge*t_hrs*0.1
		# 			amount = yacht_obj.price_charge*t_hrs+addamt
		# 			vals['amount_total'] = yacht_obj.price_charge*t_hrs+addamt
		# if yacht_obj.charge_name == "Weekday":
		# 		if cruise_date.weekday() == 0 or cruise_date.weekday() == 1 or cruise_date.weekday() == 2 or cruise_date.weekday() == 3 or cruise_date.weekday() == 6:
		# 			vals['cost_per_hr'] = yacht_obj.price_charge
		# 			addamt= yacht_obj.price_charge*t_hrs*0.1
		# 			amount = yacht_obj.price_charge*t_hrs+addamt
		# 			vals['amount_total'] = yacht_obj.price_charge*t_hrs+addamt
		return super(booking_yachts, self).write(cr, uid, ids, vals, context=context)
		# return True

		
	def onchange_time(self,cr,uid,ids,time1,time2,cost_per_hr,half_amt_received,context=None):
		res = {'value':{}}
		t_hrs = time1-time2
		if t_hrs < 0:
			t_hrs = (t_hrs)*(-1)
		total = (cost_per_hr*t_hrs) * 0.1
		res['value'].update({'total_hrs':t_hrs,'amount_total':(cost_per_hr*t_hrs) + total})
		if half_amt_received == 'yes':
			res['value'].update({'amount_received':res['value']['amount_total']/2,
				'amt_bal':res['value']['amount_total']/2})
		return res

	def onchange_cost_per_hr(self,cr,uid,ids,cost_per_hr,context=None):
		res = {'value':{}}
		if ids:
			bkng_obj = self.pool.get('booking.yachts').browse(cr,uid,ids[0])
			# print "total hours",bkng_obj.total_hrs
			# print bkng_obj.security_deposit
			# print cost_per_hr
			add_amt = bkng_obj.total_hrs*cost_per_hr *0.1
			res['value'].update({'amount_total':bkng_obj.total_hrs*cost_per_hr+add_amt})
		return res

	def onchange_yacht(self,cr,uid,ids,yacht_id,context=None):
		res = {'value':{}}
		y_obj1 = self.pool.get('yatch.config').browse(cr,uid,yacht_id,context=None)
		res['value'].update({'no_guests':y_obj1.max_no_pass})
		yacht = self.pool.get('yacht.charges.line').search(cr,uid,[('y_id','=',yacht_id)])
		if yacht:
			y_obj = self.pool.get('yacht.charges.line').browse(cr,uid,yacht[0],context=None)
			res['value'].update({'cost_per_hr':y_obj.price_charge,'amount_received':y_obj1.min_dep})
		else:
			res['value'].update({'cost_per_hr':0.0})
		return res

	def onchange_amt(self,cr,uid,ids,amount_total,half_amt_received,context=None):
		res = {'value':{}}
		if half_amt_received == True:
			res['value'].update({'amount_received':amount_total/2,'amt_bal':amount_total/2})
		else:
			if ids:
				booking_obj = self.pool.get('booking.yachts').browse(cr,uid,ids[0])
				res['value'].update({'amount_received':booking_obj.yacht_id.min_dep,'amt_bal':booking_obj.yacht_id.min_dep})
		return res

	def onchange_user(self,cr,uid,ids,booked_by,context=None):
		res = {'value':{}}
		user_obj = self.pool.get('res.users').browse(cr,uid,booked_by)
		if booked_by:
			res['value'].update({'signature':user_obj.signature,'phone':user_obj.phone})
		else:
			res['value'].update({'signature':'','phone':''})
		return res

	def onchange_client(self,cr,uid,ids,client_id,context=None):
		res = {'value':{}}
		partner_obj = self.pool.get('res.partner').browse(cr,uid,client_id)
		if client_id:
			res['value'].update({'contact_num':partner_obj.phone})
		else:
			res['value'].update({'contact_num':''})
		return res

	def onchange_booking_type(self,cr,uid,ids,book_for,yacht_id,context=None):
		res = {'value':{}}
		if ids:
			booking_yacht = self.pool.get('booking.yachts').browse(cr,uid,ids[0])
			cruise_date = datetime.datetime.strptime(booking_yacht.cruise_date, "%Y-%m-%d")
			yacht = self.pool.get('yacht.charges.line').search(cr,uid,[('y_id','=',yacht_id),('charge_type','=',book_for)])	

			# if cruise_date.weekday() == 0:
			# 	print "Monday"
			# if cruise_date.weekday() == 1:
			# 	print "Tuesday"
			# if cruise_date.weekday() == 2:
			# 	print "Wednesday"
			# if cruise_date.weekday() == 3:
			# 	print "thrusday"
			# if cruise_date.weekday() == 4:
			# 	print "Friday"
			# if cruise_date.weekday() == 5:
			# 	print "Saturday"
			# if cruise_date.weekday() == 6:
			# 	print "Sunday"

			for y in yacht:
				y_obj = self.pool.get('yacht.charges.line').browse(cr,uid,y,context=None)
				# charge_ids = self.pool.get('yacht.charges').search(cr,uid,[('id','!=',False)])
				charge_ids = self.pool.get('yacht.charges').browse(cr,uid,y_obj.charge_id.id)
				# print y_obj.charge_id.id
				# print charge_ids.id
				if y_obj.charge_id.charge_name == "Weekend":
					if cruise_date.weekday() == 5 or cruise_date.weekday() == 4:
						# yacht_idss = self.pool.get('yacht.charges.line').search(cr,uid,[('y_id','=',yacht_id),('charge_type','=',book_for)])
						# yacht = self.pool.get('yacht.charges').search(cr,uid,[('charge_name','=',name_crg),('charge_type','=',charge_type)])
						# yacht_obj = self.pool.get('yacht.charges').browse(cr,uid,yacht[0])
						res['value'].update({'cost_per_hr':y_obj.price_charge})
				if y_obj.charge_id.charge_name == "Weekday":
					if cruise_date.weekday() == 0 or cruise_date.weekday() == 1 or cruise_date.weekday() == 2 or cruise_date.weekday() == 3 or cruise_date.weekday() == 6:
						# yacht_line_obj = self.pool.get('yacht.charges.line').browse(cr,uid,yacht_id)
						# yacht = self.pool.get('yacht.charges').search(cr,uid,[('charge_name','=',name_crg),('charge_type','=',charge_type)])
						# yacht_obj = self.pool.get('yacht.charges').browse(cr,uid,yacht[0])
						res['value'].update({'cost_per_hr':y_obj.price_charge})
		return res

	def status_approve(self,cr,uid,ids,context=None):
		self.pool.get('booking.yachts').write(cr,uid,ids,{'state':'approved'})
		return True

	def cancel_booking(self,cr,uid,ids,context=None):
		self.pool.get('booking.yachts').write(cr,uid,ids,{'state':'cancel'})
		return True

	def create_quotation(self,cr,uid,ids,context=None):
		for i in self.browse(cr,uid,ids):
			y_id = self.pool.get('charges.line').search(cr,uid,[('charge_n_yacht','=',i.yacht_id.yatch_name)],context=None)
			if not y_id:
				y_id = self.pool.get('charges.line').create(cr,uid,{'charge_n_yacht':i.yacht_id.yatch_name},context=None)
			else:
				y_id=y_id[0]
			y_obj = self.pool.get('charges.line').browse(cr,uid,y_id,context=None)

			addr_id = self.pool.get('res.partner').address_get(cr, uid, [i.client_id.id], ['delivery'])['delivery'],
			pu = (i.cost_per_hr*0.1) + i.cost_per_hr
			# discount = 0.0
			# if i.client_id.is_agent==True:
			# 	discount = 0.15
			# if i.client_id.is_saleperson==True:
			# 	discount = 0.05
			# if i.client_id.is_manager==True:
			# 	discount = 0.1

			vals={'origin': False,
			'booking_id':i.id,
			'message_follower_ids': [],
			'order_line': [[0, False, {'product_uos_qty': 1,
			'yacht_id': y_obj.id, 
			'product_id': False, 
			'product_uom': 1, 
			'sequence': 10, 
			'invoice_lines': [], 
			'price_unit': pu, 
			'product_uom_qty': 1, 
			'name': y_obj.charge_n_yacht, 
			'state': 'draft', 
			'address_allotment_id': False, 
			'th_weight': 0.0, 
			'product_uos': False, 
			'discount': i.client_id.discount, 
			'book_for': i.book_for, 
			'type': u'make_to_stock', 
			'tax_id': [(6, 0, [])]}]],
			'order_policy': u'manual', 
			'invoice_ids': [], 
			'shop_id': 1, 
			'client_order_ref': False, 
			'partner_invoice_id': i.client_id.id, 
			# 'date_order': '2014-08-06', 
			'partner_id': i.client_id.id, 
			'date_confirm': False, 
			'fiscal_position': False, 
			'user_id': uid, 
			'partner_shipping_id': addr_id, 
			'payment_term': False, 
			'message_ids': [], 
			'note': False, 
			'state': 'draft', 
			'invoice_quantity': u'order', 
			'pricelist_id': 1, 
			'project_id': False}
			if i.catering==True:
				l = [0,False]
				y_id = self.pool.get('charges.line').search(cr,uid,[('charge_n_yacht','=','Catering')],context=None)
				if not y_id:
					y_id = self.pool.get('charges.line').create(cr,uid,{'charge_n_yacht':'Catering'},context=None)
				else:
					y_id=y_id[0]
				y_obj = self.pool.get('charges.line').browse(cr,uid,y_id,context=None)
				# t=(0,0)
				d={}
				d.update({'yacht_id':y_obj.id,'name': y_obj.charge_n_yacht,'product_uom_qty': 1,'book_for': i.book_for,})#,'bucket_name': obj.product_id.id,'weight': obj.weight})
				# t+=(d,)
				l.append(d)
				vals['order_line'].append(l)
				# vals.update({'order_line':l})

			if i.water_sports==True:
				l = [0,False]
				y_id = self.pool.get('charges.line').search(cr,uid,[('charge_n_yacht','=','Water Sports')],context=None)
				if not y_id:
					y_id = self.pool.get('charges.line').create(cr,uid,{'charge_n_yacht':'Water Sports'},context=None)
				else:
					y_id=y_id[0]
				y_obj = self.pool.get('charges.line').browse(cr,uid,y_id,context=None)
				# t=(0,0)
				d={}
				d.update({'yacht_id':y_obj.id,'name': y_obj.charge_n_yacht,'product_uom_qty': 1,'book_for': i.book_for,})#,'bucket_name': obj.product_id.id,'weight': obj.weight})
				# t+=(d,)
				l.append(d)
				vals['order_line'].append(l)
				# vals.update({'order_line':l})

			if i.client_bring_alcohol==False:
				l = [0,False]
				y_id = self.pool.get('charges.line').search(cr,uid,[('charge_n_yacht','=','Alcohol')],context=None)
				if not y_id:
					y_id = self.pool.get('charges.line').create(cr,uid,{'charge_n_yacht':'Alcohol'},context=None)
				else:
					y_id=y_id[0]
				y_obj = self.pool.get('charges.line').browse(cr,uid,y_id,context=None)
				# t=(0,0)
				d={}
				d.update({'yacht_id':y_obj.id,'name': y_obj.charge_n_yacht,'product_uom_qty': 1,'book_for': i.book_for,})#,'bucket_name': obj.product_id.id,'weight': obj.weight})
				# t+=(d,)
				l.append(d)
				vals['order_line'].append(l)
				# vals.update({'order_line':l})

			# if i.client_bring_alcohol==False:
			# 	l = [0,False]
			# 	y_id = self.pool.get('charges.line').search(cr,uid,[('charge_n_yacht','=','Alcohol')],context=None)
			# 	if not y_id:
			# 		y_id = self.pool.get('charges.line').create(cr,uid,{'charge_n_yacht':'Alcohol'},context=None)
			# 	else:
			# 		y_id=y_id[0]
			# 	y_obj = self.pool.get('charges.line').browse(cr,uid,y_id,context=None)
			# 	# t=(0,0)
			# 	d={}
			# 	d.update({'yacht_id':y_obj.id,'name': y_obj.charge_n_yacht,'product_uom_qty': i.no_guests,'book_for': i.book_for,})#,'bucket_name': obj.product_id.id,'weight': obj.weight})
			# 	# t+=(d,)
			# 	l.append(d)
			# 	vals['order_line'].append(l)
			# 	# vals.update({'order_line':l})

			if i.own_food==False:
				l = [0,False]
				y_id = self.pool.get('charges.line').search(cr,uid,[('charge_n_yacht','=','Food')],context=None)
				if not y_id:
					y_id = self.pool.get('charges.line').create(cr,uid,{'charge_n_yacht':'Food'},context=None)
				else:
					y_id=y_id[0]
				y_obj = self.pool.get('charges.line').browse(cr,uid,y_id,context=None)
				# t=(0,0)
				d={}
				d.update({'yacht_id':y_obj.id,'name': y_obj.charge_n_yacht,'product_uom_qty': 1,'book_for': i.book_for,})#,'bucket_name': obj.product_id.id,'weight': obj.weight})
				# t+=(d,)
				l.append(d)
				vals['order_line'].append(l)
				# vals.update({'order_line':l})

			if i.decoration==True:
				l = [0,False]
				y_id = self.pool.get('charges.line').search(cr,uid,[('charge_n_yacht','=','Decoration')],context=None)
				if not y_id:
					y_id = self.pool.get('charges.line').create(cr,uid,{'charge_n_yacht':'Decoration'},context=None)
				else:
					y_id=y_id[0]
				y_obj = self.pool.get('charges.line').browse(cr,uid,y_id,context=None)
				# t=(0,0)
				d={}
				d.update({'yacht_id':y_obj.id,'name': y_obj.charge_n_yacht,'product_uom_qty': 1,'book_for': i.book_for,})#,'bucket_name': obj.product_id.id,'weight': obj.weight})
				# t+=(d,)
				l.append(d)
				vals['order_line'].append(l)
				# vals.update({'order_line':l})

			if i.dj==True:
				l = [0,False]
				y_id = self.pool.get('charges.line').search(cr,uid,[('charge_n_yacht','=','DJ')],context=None)
				if not y_id:
					y_id = self.pool.get('charges.line').create(cr,uid,{'charge_n_yacht':'DJ'},context=None)
				else:
					y_id=y_id[0]
				y_obj = self.pool.get('charges.line').browse(cr,uid,y_id,context=None)
				# t=(0,0)
				d={}
				d.update({'yacht_id':y_obj.id,'name': y_obj.charge_n_yacht,'product_uom_qty': 1,'book_for': i.book_for,})#,'bucket_name': obj.product_id.id,'weight': obj.weight})
				# t+=(d,)
				l.append(d)
				vals['order_line'].append(l)
				# vals.update({'order_line':l})

			if i.luxury_transportation==True:
				l = [0,False]
				y_id = self.pool.get('charges.line').search(cr,uid,[('charge_n_yacht','=','Luxury Transportation')],context=None)
				if not y_id:
					y_id = self.pool.get('charges.line').create(cr,uid,{'charge_n_yacht':'Luxury Transportation'},context=None)
				else:
					y_id=y_id[0]
				y_obj = self.pool.get('charges.line').browse(cr,uid,y_id,context=None)
				# t=(0,0)
				d={}
				d.update({'yacht_id':y_obj.id,'name': y_obj.charge_n_yacht,'product_uom_qty': 1,'book_for': i.book_for,})#,'bucket_name': obj.product_id.id,'weight': obj.weight})
				# t+=(d,)
				l.append(d)
				vals['order_line'].append(l)
				# vals.update({'order_line':l})

			self.pool.get('sale.order').create(cr,uid,vals,context=None)
		self.pool.get('booking.yachts').write(cr,uid,ids,{'state':'quotation'})
		return True

	def send_mail(self,cr,uid,context=None):
		m_ids = self.pool.get('ir.mail_server').search(cr,uid,[('active','=','True')])
		mail_obj = self.pool.get('ir.mail_server').browse(cr,uid,m_ids[0],context)
		count = self.search(cr,uid,[('amount_received','=',0),('state','=','draft')])
		for cust in count:
			obj=self.browse(cr,uid,cust)
			username =mail_obj.smtp_user
			password =mail_obj.smtp_pass
			host = mail_obj.smtp_host
			port = mail_obj.smtp_port
			fromaddr = username
			server = smtplib.SMTP(host+':'+'587')
			server.ehlo()
			server.starttls()
			server.ehlo()
			server.login(username, password)
			msg = MIMEMultipart()
			msg['From'] = fromaddr
			msg['Subject'] = 'Royal Yachts Booking Information'
			toaddr =obj.mail
			msg['To'] = toaddr
			text = ('<p><h2>Hello Sir/Madam,</h2><h4>We have not yet received your amount for booking.</p><p><b>Kindly pay your bill to ensure us your booking.</b></p><p>Your booking will be cancelled in next 6 hrs if we do not get any response from your side.</p><p>Thank You,</p><p>Team Royal Yachts</p></h4>')
			body = MIMEText(text, _subtype='html')
			msg.attach(body)
			server.sendmail(fromaddr, toaddr, msg.as_string())
			server.quit()
		return True


	# def sending_mail(self, cr, uid, context=None):
	# 	booking_ids = self.pool.get('booking.yachts').search(cr,uid,[('id','!=',False)])
	# 	for b_id in booking_ids:
	# 		email_list=[]
	# 		booking_obj = self.pool.get('booking.yachts').browse(cr,uid,b_id)
	# 		cust_obj = self.pool.get('res.partner').browse(cr,uid,booking_obj.client_id.id)
	# 		yacht_obj = self.pool.get('yatch.config').browse(cr,uid,booking_obj.yacht_id.id)
	# 		if (booking_obj.total_hrs == yacht_obj.ser_time_prd):
	# 			m_ids = self.pool.get('ir.mail_server').search(cr,uid,[('active','=','True')])
	# 			mail_obj = self.pool.get('ir.mail_server').browse(cr,uid,m_ids[0],context)
	# 			email_list.append(yacht_obj.cap_email)
	# 			email_list.append(yacht_obj.cap_name.parent_id.work_email)
	# 			print email_list
	# 			username =mail_obj.smtp_user
	# 			password =mail_obj.smtp_pass
	# 			host = mail_obj.smtp_host
	# 			port = mail_obj.smtp_port
	# 			fromaddr = username
	# 			server = smtplib.SMTP(host+':'+'587')
	# 			server.ehlo()
	# 			server.starttls()
	# 			server.ehlo()
	# 			server.login(username, password)
	# 			msg = MIMEMultipart()
	# 			msg['From'] = fromaddr
	# 			msg['Subject'] = 'Royal Yachts Booking Information'
	# 			toaddr = email_list 
	# 			msg['To'] =", ".join(email_list)
	# 			text = ('<p><h2>Hello Sir/Madam</h2><h4>Test message.</p><p><b>Service time and total cruising time both are equal.</b></p>')
	# 			body = MIMEText(text, _subtype='html')
	# 			msg.attach(body)
	# 			server.sendmail(fromaddr, email_list, msg.as_string())
	# 			server.quit()
	# 	return True


booking_yachts()




class prepare_quotation(osv.osv):

	_inherit="sale.order"

	_columns={
	'booking_id':fields.many2one('booking.yachts','Booking ID'),
	}

	def _get_default_shop(self, cr, uid, context=None):
		company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
		shop_ids = self.pool.get('sale.shop').search(cr, uid, [('company_id','=',company_id)], context=context)
		if not shop_ids:
			raise osv.except_osv(_('Error!'), _('There is no default shop for the current user\'s company!'))
		return shop_ids[0]

	_defaults = {
		'date_order': fields.date.context_today,
		'order_policy': 'manual',
		'state': 'draft',
		'user_id': lambda obj, cr, uid, context: uid,
		'name': lambda obj, cr, uid, context: '/',
		'invoice_quantity': 'order',
		'shop_id': _get_default_shop,
		'partner_invoice_id': lambda self, cr, uid, context: context.get('partner_id', False) and self.pool.get('res.partner').address_get(cr, uid, [context['partner_id']], ['invoice'])['invoice'],
		'partner_shipping_id': lambda self, cr, uid, context: context.get('partner_id', False) and self.pool.get('res.partner').address_get(cr, uid, [context['partner_id']], ['delivery'])['delivery'],
	}

	def create(self, cr, uid, vals, context=None):
		if vals.get('name','/')=='/':
			vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'sale.order') or '/'
		return super(prepare_quotation, self).create(cr, uid, vals, context=context)

	def action_button_confirm(self, cr, uid, ids, context=None):
		assert len(ids) == 1, 'This option should only be used for a single id at a time.'
		wf_service = netsvc.LocalService('workflow')
		s_obj = self.browse(cr,uid,ids[0])
		wf_service.trg_validate(uid, 'sale.order', ids[0], 'order_confirm', cr)
		self.pool.get('booking.yachts').write(cr,uid,s_obj.booking_id.id,{'state':'done'})

		# redisplay the record as a sales order
		view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'sale', 'view_order_form')
		view_id = view_ref and view_ref[1] or False,
		return {
			'type': 'ir.actions.act_window',
			'name': _('Sales Order'),
			'res_model': 'sale.order',
			'res_id': ids[0],
			'view_type': 'form',
			'view_mode': 'form',
			'view_id': view_id,
			'target': 'current',
			'nodestroy': True,
		}




prepare_quotation()

class prepare_order_line(osv.osv):

	def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
		cur_obj = self.pool.get('res.currency')
		res = {}
		c = 0
		if context is None:
			context = {}
		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = {
						'serial_no': 0,

			}
			c = c + 1
			res[line.id]['serial_no'] = c
		return res

	_inherit="sale.order.line"

	_columns={
	'name': fields.text('Description', required=True, readonly=True, states={'draft': [('readonly', False)]}),
	'serial_no':fields.function(_amount_line, string='Sl.', type='integer',multi="sums"),
	'book_for':fields.selection([('hour', 'Hourly'), ('day', 'Daily'),('week', 'Weekly')], 'Book For'),
	# 'cost_per_head':fields.float('Cost Per Head'),
	'product_uom_qty': fields.integer('No. of Persons', digits_compute= dp.get_precision('Product UoS'), required=True, readonly=True, states={'draft': [('readonly', False)]}),
	'yacht_id':fields.many2one('charges.line','Yacht/Charges'),
	'price_unit': fields.float('Cost per Head', required=True, digits_compute= dp.get_precision('Product Price'), readonly=True, states={'draft': [('readonly', False)]}),
	}

	def onchange_yacht_id(self,cr,uid,ids,yacht_id,context=None):
		res = {'value':{}}
		# yacht = self.pool.get('yacht.charges.line').search(cr,uid,[('y_id','=',yacht_id)])
		# if yacht:
		# 	y_obj = self.pool.get('yacht.charges.line').browse(cr,uid,yacht[0],context=None)
		# 	res['value'].update({'cost_per_hr':y_obj.price_charge})
		# else:
		# 	res['value'].update({'cost_per_hr':0.0})
		# return res
		y_obj = self.pool.get('charges.line').browse(cr,uid,yacht_id,context=None)
		res['value'].update({'name':y_obj.charge_n_yacht})
		# else:
		# 	res['value'].update({'name':y_obj.yatch_name})
		return res

	def onchange_booking_type(self,cr,uid,ids,book_for,yacht_id,context=None):
		if not yacht_id:
			raise osv.except_osv(_('No Yacht is Selected!'),
							_('Please Select a Yacht 1st.'))
		res = {'value':{}}
		yacht = self.pool.get('yacht.charges.line').search(cr,uid,[('y_id','=',yacht_id),('charge_type','=',book_for)])
		if yacht:
			y_obj = self.pool.get('yacht.charges.line').browse(cr,uid,yacht[0],context=None)
			res['value'].update({'price_unit':y_obj.price_charge})
		else:
			res['value'].update({'price_unit':0.0})
		return res

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
				# 'partner_id':line.order_id.partner_id.id,
				'price_unit': pu,
				'quantity': uosqty,
				'discount': line.discount,
				'uos_id': uos_id,
				'product_id': line.product_id.id or False,
				'yacht_id' : line.yacht_id.id,
				'book_for':line.book_for,
				'invoice_line_tax_id': [(6, 0, [x.id for x in line.tax_id])],
				'account_analytic_id': line.order_id.project_id and line.order_id.project_id.id or False,
			}

		return res

prepare_order_line()


class account_invoice_line_inherit(osv.osv):


	_inherit = 'account.invoice.line'

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

	_columns = {
		 'name': fields.text('Description', required=True),
		 'book_for':fields.selection([('hour', 'Hourly'), ('day', 'Daily'),('week', 'Weekly')], 'Book For'),
		 'serial_no_invoice':fields.function(serial_inc,string='Sl.No',type="integer",multi="sums" ,readonly=True),
		 'yacht_id':fields.many2one('charges.line','Yacht/Charges'),
		 'price_unit': fields.float('Cost per Head', required=True, digits_compute= dp.get_precision('Product Price')),
		 'quantity': fields.integer('No. of Persons', digits_compute= dp.get_precision('Product Unit of Measure'), required=True),

	}

# 	def onchange_subtotal(self,cr,uid,ids,no_adults,no_childs,yacht_line_id,context=None):
# 		print context
# 		# if not yacht_id:
# 		# 	raise osv.except_osv(_('No Yacht is Selected'),_("Please Select a Yacht first !") )
# 		res = {'value':{}}
# 		br_obj = self.browse(cr,uid,ids[0])
# 		y_obj = self.pool.get('booking.yachts').browse(cr,uid,br_obj.yacht_id.id,context=None)
# 		res['value'].update({'sub_total':(int(no_adults)*y_obj.yacht_id.price_adult) + (int(no_childs)*y_obj.yacht_id.price_children)})
# 		return res	

account_invoice_line_inherit()


class charges_line(osv.osv):
	_name="charges.line"

	_rec_name="charge_n_yacht"

	_columns={
	'charge_n_yacht' : fields.char('Charge Name'),
	}

charges_line()

class res_partner_employee(osv.osv):
	
	_inherit="hr.employee"

	def create(self, cr, uid, data, context=None):
		employee_id = super(res_partner_employee, self).create(cr, uid, data, context=context)
		vals={'name':data['name'],'email':data['work_email'],'phone':data['work_phone'],'customer_type':'internal'}
		self.pool.get('res.partner').create(cr,uid,vals)
		try:
			(model, mail_group_id) = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'mail', 'group_all_employees')
			employee = self.browse(cr, uid, employee_id, context=context)
			self.pool.get('mail.group').message_post(cr, uid, [mail_group_id],
				body=_('Welcome to %s! Please help him/her take the first steps with OpenERP!') % (employee.name),
				subtype='mail.mt_comment', context=context)
		except:
			pass # group deleted: do not push a message
		return employee_id

res_partner_employee()

class res_partner_change(osv.osv):
	
	_inherit="res.partner"
	_columns={

		'customer_type':fields.selection([('normal','Normal Customer'),('agent','Agent'),('internal','Internal'),('manager','Manager')],'Customer Type'),
		'discount':fields.float('Discount'),
		'is_agent':fields.boolean('Agent'),
		'is_saleperson':fields.boolean('Sale Person'),
		'is_manager':fields.boolean('Manager'),
	} 

	def onchange_customer(self,cr,uid,ids,is_agent,is_saleperson,is_manager,context=None):
		vals = {}
		if is_agent == True:
			vals.update({'is_saleperson':False,'is_manager':False,'discount':0.15})
		return {'value' : vals}

	def onchange_customer1(self,cr,uid,ids,is_agent,is_saleperson,is_manager,context=None):
		vals = {}
		if is_saleperson == True:
			vals.update({'is_agent':False,'is_manager':False,'discount':0.05})
		return {'value' : vals}

	def onchange_customer2(self,cr,uid,ids,is_agent,is_saleperson,is_manager,context=None):
		vals = {}
		if is_manager == True:
			vals.update({'is_saleperson':False,'is_agent':False,'discount':0.10})
		return {'value' : vals}  
res_partner_change()