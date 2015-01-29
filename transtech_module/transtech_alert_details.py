from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
class alert_section(osv.osv):
	
	_name = "alert.info"
	
	#_inherit = ['mail.thread','ir.needaction_mixin']

	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
		default.update({
			'name': self.pool.get('ir.sequence').get(cr, uid, 'alert.info'),
			})

		return super(alert_section, self).copy(cr, uid, id, default, context=context)

	def _login_customer(self,cr,uid,ids,name,arg,context=None):
		customerid = self.pool.get('res.users').search(cr, uid, [('id', '=', uid)], context=context)
		customerid_name =self.pool.get('res.users').browse(cr, uid, customerid, context=context)
		print customerid_name[0].name
		customer_info = self.pool.get('customer.info').search(cr, uid, [('name', '=', customerid_name[0].name)], context=context)
		customer_info_name = self.pool.get('customer.info').browse(cr, uid,customer_info, context=context)
		print customer_info_name[0].id
		return customer_info_name[0].id

          
	_columns = {
		'name':fields.char('Alert ID',readonly=True),
		'customer':fields.many2one('customer.info','Customer', required=False),
		#'customer':fields.function(_login_customer,type="many2one",relation="customer.info",string='Customer',required=False),
		'atm_id':fields.many2one('atm.info','ATM', required=True,domain="[('customer','=',customer)]"),
		'category':fields.selection([('complaint','Complaint'),('issue','Issue')],'Category',required=True),
		'priority':fields.selection([('low','Low'),('medium','Medium'), ('high','High'),('critical','Critical')],'Priority',required=True),
		'country_id':fields.many2one('res.country','Country',domain="[('code','=','AE')]"),
		'state_id':fields.many2one('res.country.state','State', domain="[('country_id','=',country_id)]"),
		#'assign_to':fields.many2one('res.users','Assign To', required=True, domain="[('role','=','Surveyor')]"),
		'status':fields.selection([('assigned','Assigned'),('resolved','Resolved'), ('closed','Closed')],'Status',required=True,track_visibility='always'),
		'summary':fields.char('Summary', size=100, required=False),
		'description':fields.text('Description'),
		'reason_id':fields.many2one('reason.code','Reason Code'),
		'reason_disc':fields.text('Reason Descriptions'),
	}

	def _default_country(self, cr, uid, context=None):
		cid = self.pool.get('res.country').search(cr, uid, [('code', '=', 'AE')], context=context)
		return cid[0]		
			
	
	_defaults = {
		'status':'assigned',
		'country_id':_default_country,
         	
	}
	_order = "name desc"
	
	def create(self,cr,uid,vals,context=None):
		if vals.get('name','/') == '/': 
			vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'alert.info') or '/'
		alert_id = super(alert_section, self).create(cr, uid, vals, context=context)
		#print alert_id
		alert_info = self.browse(cr,uid,[alert_id],context=None)[0]
		#print alert_info.name
		alertnumber = alert_info.name
		#print alert_id.name
		#print alertnumber[0:5]
		if alert_id != False and alertnumber[0:5]=='Alert':
			self.send_alert_invitation_customer(cr,uid,[alert_id],context=None)
			self.send_alert_invitation_teamleader(cr,uid,[alert_id],context=None)
		return alert_id

	def status_resolve(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'resolved'},context=context)
		return True

	def status_close(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'closed'},context=context)
		return True

	def unlink(self, cr, uid, ids, context=None):
        	alert_obj = self.pool.get('alert.info').browse(cr,uid,ids[0])
		if alert_obj.status in ('resolved','closed'):
			raise osv.except_osv(_('Invalid Action!'), _("You can't delete an Alert which is either in 'Resolved state' or in 'Closed state' "))
        	
        	return super(alert_section, self).unlink(cr, uid, ids, context=context)

	def send_alert_invitation_customer(self,cr,uid,ids,context=None):
		alert_obj = self.browse(cr,uid,ids,context=None)[0]
		#print alert_obj
		
		customer_id =  self.pool.get('customer.info').browse(cr,uid,alert_obj.customer.id)
		customer_name = customer_id.name
		atm_id1 =self.pool.get('atm.info').browse(cr,uid,alert_obj.atm_id.id)
		atm_name = atm_id1.name
		#user_ids = self.pool.get('res.users').browse(cr,uid,alert_obj.assign_to.id)
		#print user_ids.name_tl
		#teamleader_find = self.pool.get('res.users').browse(cr,uid,user_ids.name_tl.id)
		#print teamleader_find
		#temail_id = teamleader_find.email
		#print temail_id
		if not customer_id.contact_email:
			raise osv.except_osv(_('No Email Provided for this customer'),_("Please give a Valid email address !") )
			return False
		#tname= teamleader_find.name
		mail_ids = self.pool.get('ir.mail_server').search(cr,uid,[('active','=','True')])
		mail_obj = self.pool.get('ir.mail_server').browse(cr,uid,mail_ids)[0]
		username = mail_obj.smtp_user
		pwd = mail_obj.smtp_pass
		host = mail_obj.smtp_host
		port = mail_obj.smtp_port
		fromaddr = username
		server = smtplib.SMTP(host+':'+'587')
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(username, pwd)
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['Subject'] = 'Regarding Alert created in TransTech Portal'
		toaddr = customer_id.contact_email
		msg['To'] = toaddr
		text = ('<p><h2>Dear %s,</h2>We got an information of alert which you have created in our portal.</p><p><b>Details of generate alerts is given below:-</b></p><p><b>Alert Category </b> : %s</p><p><b>Priority </b>:%s</p><p><b>ATM </b>:%s,%s</p><p>We will look over this problem and resolve it as soon as possible</p>')%(customer_id.name,alert_obj.category,alert_obj.priority,atm_name,atm_id1.atm_id)
		body = MIMEText(text, _subtype='html')
		msg.attach(body)
		res = server.sendmail(fromaddr, toaddr, msg.as_string())
		server.quit()

		return True

	def send_alert_invitation_teamleader(self,cr,uid,ids,context=None):
		alert_obj = self.browse(cr,uid,ids,context=None)[0]
		#print alert_obj
		customer_id =  self.pool.get('customer.info').browse(cr,uid,alert_obj.customer.id)
		customer_name = customer_id.name
		atm_id1 =self.pool.get('atm.info').browse(cr,uid,alert_obj.atm_id.id)
		atm_name = atm_id1.name
		user_ids = self.pool.get('res.users').browse(cr,uid,customer_id.account_manager.id)
		#print user_ids.name_tl
		#teamleader_find = self.pool.get('res.users').browse(cr,uid,user_ids.name_tl.id)
		#print teamleader_find
		temail_id = user_ids.email
		#print temail_id
		if not temail_id:
			raise osv.except_osv(_('No Email Provided for this customer'),_("Please give a Valid email address !") )
			return False
		tname= user_ids.name
		mail_ids = self.pool.get('ir.mail_server').search(cr,uid,[('active','=','True')])
		mail_obj = self.pool.get('ir.mail_server').browse(cr,uid,mail_ids)[0]
		username = mail_obj.smtp_user
		pwd = mail_obj.smtp_pass
		host = mail_obj.smtp_host
		port = mail_obj.smtp_port
		fromaddr = username
		server = smtplib.SMTP(host+':'+'587')
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(username, pwd)
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['Subject'] = 'New Customer Alert in Transtech Portal'
		toaddr = temail_id
		msg['To'] = toaddr
		text = ('<p><h2>Hello %s,</h2> One Customer Alert is recorded in Transtech Portal</p><p><b>Details of generate alerts is given below:-</b></p><p><b>Genrated By </b>: %s</p><p><b>Alert ID</b> :  %s</p><p><b>Alert Category </b> : %s</p><p><b>Priority </b>:%s</p><p><b>ATM </b>:%s,%s</p>')%(tname,customer_id.name,alert_obj.name,alert_obj.category,alert_obj.priority,atm_name,atm_id1.atm_id)
		body = MIMEText(text, _subtype='html')
		msg.attach(body)
		res = server.sendmail(fromaddr, toaddr, msg.as_string())
		server.quit()

		return True
alert_section()
