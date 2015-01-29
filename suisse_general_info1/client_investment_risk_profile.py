from openerp.osv import fields, osv
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import time
import datetime

class client_investment_risk_profile(osv.osv):
	_name='client.investment.risk.profile'
	_description='Investment Risk Profile'
	#_inherit='purchase.order'
		

	_columns = {
		'name':fields.char('Client details',select=True,readonly=True),
		'relationship_title':fields.many2one('suisse.client.general.info','Relationship Title',select=True,change_default=True, required=True,track_visibility='always'),
		#Financial Information Question 1
		'question_one_one':fields.boolean('Self employed/own business'),
		'question_one_two':fields.boolean('Employee'),
		'question_one_three':fields.boolean('Retired'),
		'question_one_four':fields.boolean('Student'),
		'question_one_five':fields.boolean('Home maker'),
		'investment_client_one':fields.char('Client one'),
		'investment_client_two':fields.char('Client Two'),
		#Financial Information Question 2
		'question_two_one':fields.boolean('I am below 64 years old'),
		'question_two_two':fields.boolean('I am 64 years or more,and below 80 years old'),
		'question_two_three':fields.boolean('I am 80 years or more'),
		#Financial Information Question 3
		'question_three_one':fields.boolean('Less than 3 years'),
		'question_three_two':fields.boolean('3 years or more'),
		'question_three_three':fields.boolean('No definable time horizon'),
		#Financial Information Question 4
		'question_four_one':fields.boolean('Less than 25%'),
		'question_four_two':fields.boolean('Between 25% and 50%'),
		'question_four_three':fields.boolean('More than 50%'),
		#Financial Information Question 5
		'question_five_one':fields.boolean('1'),
		'question_five_two':fields.boolean('2'),
		'question_five_three':fields.boolean('3'),
		#Risk Attitude Question 6
		'question_six_one':fields.boolean('1'),
		'question_six_two':fields.boolean('1'),
		'question_six_three':fields.boolean('1'),
		'question_six_four':fields.boolean('1'),
		'question_six_five':fields.boolean('1'),
		'question_six_six':fields.boolean('1'),
		'question_six_seven':fields.boolean('1'),
		#Risk Attitude Question 7
		'question_seven_one':fields.boolean('1'),
		'question_seven_two':fields.boolean('1'),
		'question_seven_three':fields.boolean('1'),
		'question_seven_four':fields.boolean('1'),
		'question_seven_five':fields.boolean('1'),
		'question_seven_six':fields.boolean('1'),
		#Risk Attitude Question 8
		'question_eight_one':fields.boolean('1'),
		'question_eight_two':fields.boolean('1'),
		'question_eight_three':fields.boolean('1'),
		'question_eight_four_one':fields.boolean('1'),
		'question_eight_four_two':fields.boolean('1'),
		'question_eight_five_one':fields.boolean('1'),
		'question_eight_five_two':fields.boolean('1'),
		'question_eight_six_one':fields.boolean('1'),
		'question_eight_six_two':fields.boolean('1'),
		'question_eight_seven_one':fields.boolean('1'),
		'question_eight_seven_two':fields.boolean('1'),
		'question_eight_eight_one':fields.boolean('1'),
		'question_eight_eight_two':fields.boolean('1'),
		'question_eight_nine_one':fields.boolean('1'),
		'question_eight_nine_two':fields.boolean('1'),
		'question_eight_ten_one':fields.boolean('1'),
		'question_eight_ten_two':fields.boolean('1'),
		'question_eight_eleven_one':fields.boolean('1'),
		'question_eight_eleven_two':fields.boolean('1'),
		'question_eight_twelve_one':fields.boolean('1'),
		'question_eight_twelve_two':fields.boolean('1'),
		'question_eight_thirteen_one':fields.boolean('1'),
		'question_eight_thirteen_two':fields.boolean('1'),
		'question_eight_fourteen_one':fields.boolean('1'),
		'question_eight_fourteen_two':fields.boolean('1'),
		'question_eight_fifteen_one':fields.boolean('1'),
		'question_eight_fifteen_two':fields.boolean('1'),
		'question_eight_sixteen_one':fields.boolean('1'),
		'question_eight_sixteen_two':fields.boolean('1'),
		#Fields For Risk Profile
		'risk_profile_one':fields.boolean('Safety Oriented'),
		'risk_profile_two':fields.boolean('Conservative'),
		'risk_profile_three':fields.boolean('Moderate'),
		'risk_profile_four':fields.boolean('Aggressive'),
		'risk_profile_five':fields.boolean('Very Aggressive'),
		'risk_profile_six':fields.boolean('Specialized Investing'),
		'risk_profile_mode_one':fields.boolean('In Person'),
		'risk_profile_mode_two':fields.boolean('Phone'),
		'risk_profile_mode_two1':fields.char('Phone'),
		'risk_profile_mode_ext':fields.integer('Ext'),
		'risk_profile_mode_date':fields.date('Profile Date'),
		'risk_profile_mode_name_staff':fields.char('Name of Staff'),
		
	}
	_defaults={
		'name':'Investment risk profile',
	}
	_order = 'relationship_title'
	
	def risk_attitude(self,cr,uid,ids,question_two_one,question_three_three,question_two_two,question_two_three,question_three_one,question_three_two,question_four_one,question_four_two,question_four_three,question_five_one,question_five_two,question_five_three,question_six_one,question_six_two,question_six_three,question_six_four,question_six_five,question_six_six,question_six_seven,question_seven_one,question_seven_two,question_seven_three,question_seven_four,question_seven_five,question_seven_six,question_eight_one,question_eight_two,question_eight_three,context=None):

		res={'value':{'question_two_one':question_two_one,'question_six_two':question_six_two,'question_six_three':question_six_three,'question_three_three':question_three_three,'question_two_two':question_two_two,'question_two_three':question_two_three,'question_three_one':question_three_one,'question_three_two':question_three_two,'question_four_one':question_four_one,'question_four_two':question_four_two,'question_four_three':question_four_three,'question_five_one':question_five_one,'question_five_two':question_five_two,'question_five_three':question_five_three,'question_six_one':question_six_one,'question_six_four':question_six_four,'question_six_five':question_six_five,'question_six_six':question_six_six,'question_six_seven':question_six_seven,'question_seven_one':question_seven_one,'question_seven_two':question_seven_two,'question_seven_three':question_seven_three,'question_seven_four':question_seven_four,'question_seven_five':question_seven_five,'question_seven_six':question_seven_six,'question_eight_one':question_eight_one,'question_eight_two':question_eight_two,'question_eight_three':question_eight_three}}
		counter=0
		count=0
		row=0
		column=0
		row_count=0
		if question_six_one==True and question_seven_one==True:
			vals={'risk_profile_one':True}
		else:
			vals={'risk_profile_one':False}
		for keys,values in res['value'].items():
			if (keys=='question_six_two' and values==True) or (keys=='question_six_three' and values==True) or (keys=='question_seven_two' and values==True):
				counter=counter+1
		if counter>=2:
			vals['risk_profile_two']=True
		else:
			vals['risk_profile_two']=False
		for keys,values in res['value'].items():
			if (keys=='question_six_four' and values==True) or (keys=='question_seven_three' and values==True) or (keys=='question_eight_one' and values==True) or (keys=='question_five_three' and values==True) :
				count=count+1
		if count>=2:
			vals['risk_profile_three']=True
		else:
			vals['risk_profile_three']=False
		for keys,values in res['value'].items():
			if (keys=='question_six_five' and values==True) or (keys=='question_six_six' and values==True) or (keys=='question_seven_four' and values==True) or (keys=='question_eight_two' and values==True) or (keys=='question_two_three' and values==True) or (keys=='question_three_one' and values==True) or (keys=='question_four_three' and values==True) or (keys=='question_five_two' and values==True):
				row=row+1
		if row>=2:
			vals['risk_profile_four']=True
		else:
			vals['risk_profile_four']=False
			
		for keys,values in res['value'].items():
			if (keys=='question_two_two' and values==True) or (keys=='question_three_two' and values==True) or (keys=='question_four_two' and values==True) or (keys=='question_seven_five' and values==True):
				row_count=row_count+1
		if row_count>=2:
			vals['risk_profile_five']=True
		else:
			vals['risk_profile_five']=False
			
		for keys,values in res['value'].items():
			if (keys=='question_six_seven' and values==True) or (keys=='question_seven_six' and values==True) or (keys=='question_eight_three' and values==True) or (keys=='question_two_one' and values==True) or (keys=='question_three_three' and values==True) or (keys=='question_four_one' and values==True) or (keys=='question_five_one' and values==True):
				column=column+1
		if column>=2:
			vals['risk_profile_six']=True
		else:
			vals['risk_profile_six']=False
		#super(client_investment_risk_profile,self).create(cr,uid,vals,context)
		return {'value': vals}
			
	# def kick_email(self,cr,uid,ids,demo1,demo2,context=None):
		# if demo1==demo2:
			# return self.trigger_email(cr,uid,ids,context)
	# def test_one_change(self,cr,uid,ids,demo1,demo2,context=None):
		# if( demo1 == demo2 ):
			# if( time.strftime("%X")== time.strftime("%X")):
				# return self.trigger_email(cr,uid,ids,context=context)
		# else : True
		
	def onchange_relationship_title(self, cr, uid, ids, relationship_title):
		res={'value':{'investment_client_one': '' ,'investment_client_two':''}}
              	suisse_client_info = self.pool.get('suisse.client.general.info')
		clients_id = suisse_client_info.browse(cr, uid,relationship_title)
		res['value'].update({'investment_client_one': clients_id.name_of_client_one,'investment_client_two':clients_id.name_of_client_two})
		#self.create(cr,uid,res)
		return res
		
	def send_email_birthday(self,cr,uid,context=None):
		mail_obj = self.pool.get('ir.mail_server').browse(cr,uid,uid,context)
		username = mail_obj.smtp_user
		password = mail_obj.smtp_pass
		host = mail_obj.smtp_host
		port = mail_obj.smtp_port
		a= time.strftime("%Y-%m-%d")
		fromaddr = username
		server = smtplib.SMTP(host+':'+'587')
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(username, password)
		rm_obj = self.pool.get('suisse.relationship.manager')
		suisse_info = self.pool.get('suisse.client.general.info')
		result = suisse_info.search(cr,uid,['|','|',('date_of_birth','!=',False),('date_of_birth_client2','!=',False),('date_of_birth_director','!=',False)])
		rm_info = self.pool.get('suisse.relationship.manager')
		read_obj = suisse_info.browse(cr,uid,result,context=context)
		for obj in read_obj:
			if obj.date_of_birth:
				if obj.date_of_birth[5:] == a[5:]:
					rm_obj = rm_info.browse(cr,uid,[obj.relationship_manager.id],context=context)
					if obj.relationship_manager.id == rm_obj[0].id:
						msg = MIMEMultipart()
						msg['From'] = fromaddr
						msg['Subject'] = 'Birthday Wishes'
						toaddr = rm_obj[0].email
						msg['To'] = toaddr
						text = ('<p><h2>Hello, %s Many Happy Returns of the Day</h2><img src="http://i.123g.us/c/birth_smiles/card/102942.gif" /></p><p>CIN Number:%s</P><p>Company:%s</p><p>Designation:%s</p>')%(obj.name_of_client_one,obj.name,obj.company_name,obj.designation)
						body = MIMEText(text, _subtype='html')
						msg.attach(body)
						server.sendmail(fromaddr, toaddr, msg.as_string())
			if obj.date_of_birth_client2:
				if obj.date_of_birth_client2[5:] == a[5:]:
					rm_obj1 = rm_info.browse(cr,uid,[obj.relationship_manager_client2.id],context=context)
					if obj.relationship_manager_client2.id ==  rm_obj1[0].id:
						msg = MIMEMultipart()
						msg['From'] = fromaddr
						msg['Subject'] = 'Birthday Wishes'
						toaddr = rm_obj1[0].email
						msg['To'] = toaddr
						text = ('<p><h2>Hello, %s Many Happy Returns of the Day</h2><img src="http://i.123g.us/c/birth_smiles/card/102942.gif" /></p><p>CIN Number:%s</P><p>Company:%s</p><p>Designation:%s</p>')%(obj.name_of_client_two,obj.name,obj.company_name_client2,obj.designation_client2)
						body = MIMEText(text, _subtype='html')
						msg.attach(body)
						server.sendmail(fromaddr, toaddr, msg.as_string())

			if obj.date_of_birth_director:
				if obj.date_of_birth_director[5:] == a[5:]:
					rm_obj2 = rm_info.browse(cr,uid,[obj.relationship_manager_director.id],context=context)
					if obj.relationship_manager_director.id ==  rm_obj2[0].id:
						msg = MIMEMultipart()
						msg['From'] = fromaddr
						msg['Subject'] = 'Birthday Wishes'
						toaddr = rm_obj2[0].email
						msg['To'] = toaddr
						text = ('<p><h2>Hello, %s Many Happy Returns of the Day</h2><img src="http://i.123g.us/c/birth_smiles/card/102942.gif" /></p><p>CIN Number:%s</P><p>Company:%s</p><p>Designation:%s</p>')%(obj.name_of_director,obj.director_cinnumber,obj.company_name_director,obj.designation_director)
						body = MIMEText(text, _subtype='html')
						msg.attach(body)
						server.sendmail(fromaddr, toaddr, msg.as_string())
		server.quit()
		return True
	def send_email_passport(self,cr,uid,context=None):
		mail_obj = self.pool.get('ir.mail_server').browse(cr,uid,uid,context)
		username = mail_obj.smtp_user
		password = mail_obj.smtp_pass
		host = mail_obj.smtp_host
		port = mail_obj.smtp_port
		a= time.strftime("%Y-%m-%d")
		c= datetime.datetime.strptime(a,'%Y-%m-%d')
		c+=datetime.timedelta(days=7)
		expiry = c.strftime('%Y-%m-%d')
		fromaddr = username
		server = smtplib.SMTP(host+':'+'587')
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(username, password)
		suisse_info = self.pool.get('suisse.client.general.info')
		passport_result = suisse_info.search(cr,uid,['|','|',('pass_validity','!=',False),('pass_validity_client2','!=',False),('pass_validity_director','!=',False)])
		rm_info = self.pool.get('suisse.relationship.manager')
		passport_read_obj = suisse_info.browse(cr,uid,passport_result,context=context)
		for pass_obj in passport_read_obj:
			if pass_obj.pass_validity:
				if pass_obj.pass_validity == expiry:
					rm_obj = rm_info.browse(cr,uid,[pass_obj.relationship_manager.id],context=context)
					if pass_obj.relationship_manager.id == rm_obj[0].id:
						msg = MIMEMultipart()
						msg['From'] = fromaddr
						msg['Subject'] = 'Alert regarding Passport'
						toaddr = rm_obj[0].email
						msg['To'] = toaddr
						text = ('<p><h2>Hello, %s Your passport is going to expire in next 7 days</h2><img src="http://i.dailymail.co.uk/i/pix/2013/07/15/article-2363965-1AD26FCD000005DC-333_468x311.jpg" /></p><p>CIN Number:%s</P><p>Company:%s</p><p>Designation:%s</p>')%(pass_obj.name_of_client_one,pass_obj.name,pass_obj.company_name,pass_obj.designation)
						body = MIMEText(text, _subtype='html')
						msg.attach(body)
						server.sendmail(fromaddr, toaddr, msg.as_string())
			if pass_obj.pass_validity_client2:
				if pass_obj.pass_validity_client2 == expiry:
					rm_obj1 = rm_info.browse(cr,uid,[pass_obj.relationship_manager_client2.id],context=context)
					if pass_obj.relationship_manager_client2.id ==  rm_obj1[0].id:
						msg = MIMEMultipart()
						msg['From'] = fromaddr
						msg['Subject'] = 'Alert regarding Passport'
						toaddr = rm_obj1[0].email
						msg['To'] = toaddr
						text = ('<p><h2>Hello, %s Your passport is going to expire in next 7 days</h2><img src="http://i.dailymail.co.uk/i/pix/2013/07/15/article-2363965-1AD26FCD000005DC-333_468x311.jpg" /></p><p>CIN Number:%s</P><p>Company:%s</p><p>Designation:%s</p>')%(pass_obj.name_of_client_two,pass_obj.name,pass_obj.company_name_client2,pass_obj.designation_client2)
						body = MIMEText(text, _subtype='html')
						msg.attach(body)
						server.sendmail(fromaddr, toaddr, msg.as_string())
			if pass_obj.pass_validity_director:
				if pass_obj.pass_validity_director == expiry:
					rm_obj2 = rm_info.browse(cr,uid,[pass_obj.relationship_manager_director.id],context=context)
					if pass_obj.relationship_manager_director.id ==  rm_obj2[0].id:
						msg = MIMEMultipart()
						msg['From'] = fromaddr
						msg['Subject'] = 'Alert regarding Passport'
						toaddr = rm_obj2[0].email
						msg['To'] = toaddr
						text = ('<p><h2>Hello, %s Your passport is going to expire in next 7 days</h2><img src="http://i.dailymail.co.uk/i/pix/2013/07/15/article-2363965-1AD26FCD000005DC-333_468x311.jpg" /></p><p>CIN Number:%s</P><p>Company:%s</p><p>Designation:%s</p>')%(pass_obj.name_of_director,pass_obj.director_cinnumber,pass_obj.company_name_director,pass_obj.designation_director)
						body = MIMEText(text, _subtype='html')
						msg.attach(body)
						server.sendmail(fromaddr, toaddr, msg.as_string())
		server.quit()
		return True
		
	def send_email_visa(self,cr,uid,context=None):
		mail_obj = self.pool.get('ir.mail_server').browse(cr,uid,uid,context)
		username = mail_obj.smtp_user
		password = mail_obj.smtp_pass
		host = mail_obj.smtp_host
		port = mail_obj.smtp_port
		a= time.strftime("%Y-%m-%d")
		c= datetime.datetime.strptime(a,'%Y-%m-%d')
		c+=datetime.timedelta(days=7)
		expiry = c.strftime('%Y-%m-%d')
		fromaddr = username
		msg['From'] = fromaddr
		server = smtplib.SMTP(host+':'+'587')
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(username, password)
		suisse_info = self.pool.get('suisse.client.general.info')
		visa_result = suisse_info.search(cr,uid,['|','|',('visa_expiry','!=',False),('visa_expiry_client2','!=',False),('visa_expiry_director','!=',False)])
		visa_read_obj = suisse_info.browse(cr,uid,visa_result,context=context)
		rm_info = self.pool.get('suisse.relationship.manager')
		for visa_obj in visa_read_obj:
			if visa_obj.visa_expiry:
				if visa_obj.visa_expiry == expiry:
					rm_obj = rm_info.browse(cr,uid,[visa_obj.relationship_manager.id],context=context)
					if visa_obj.relationship_manager.id == rm_obj[0].id:
						msg = MIMEMultipart()
						msg['Subject'] = 'Alert regarding Visa'
						toaddr = rm_obj[0].email
						msg['To'] = toaddr
						text = ('<p><h2>Hello, %s Your visa is going to expire in next 7 days</h2><img src="http://www.australiaforum.com/wp/wp-content/files/2012/04/australia-visa-stamp.jpg" /></p><p>CIN Number:%s</P><p>Company:%s</p><p>Designation:%s</p>')%(visa_obj.name_of_client_one,visa_obj.name,visa_obj.company_name,visa_obj.designation)
						body = MIMEText(text, _subtype='html')
						msg.attach(body)
						server.sendmail(fromaddr, toaddr, msg.as_string())
			if visa_obj.visa_expiry_client2:
				if visa_obj.visa_expiry_client2 == expiry:
					rm_obj1 = rm_info.browse(cr,uid,[visa_obj.relationship_manager_client2.id],context=context)
					if visa_obj.relationship_manager_client2.id ==  rm_obj1[0].id:
						msg = MIMEMultipart()
						msg['Subject'] = 'Alert regarding Visa'
						toaddr = rm_obj1[0].email
						msg['To'] = toaddr
						text = ('<p><h2>Hello, %s Your visa is going to expire in next 7 days</h2><img src="http://www.australiaforum.com/wp/wp-content/files/2012/04/australia-visa-stamp.jpg" /></p><p>CIN Number:%s</P><p>Company:%s</p><p>Designation:%s</p>')%(visa_obj.name_of_client_two,visa_obj.name,visa_obj.company_name_client2,visa_obj.designation_client2)
						body = MIMEText(text, _subtype='html')
						msg.attach(body)
						server.sendmail(fromaddr, toaddr, msg.as_string())
			if visa_obj.visa_expiry_director:
				if visa_obj.visa_expiry_director == expiry:
					rm_obj2 = rm_info.browse(cr,uid,[visa_obj.relationship_manager_director.id],context=context)
					if visa_obj.relationship_manager_director.id ==  rm_obj2[0].id:
						msg = MIMEMultipart()
						msg['Subject'] = 'Alert regarding Visa'
						toaddr = rm_obj2[0].email
						msg['To'] = toaddr
						text = ('<p><h2>Hello, %s Your visa is going to expire in next 7 days</h2><img src="http://www.australiaforum.com/wp/wp-content/files/2012/04/australia-visa-stamp.jpg" /></p><p>CIN Number:%s</P><p>Company:%s</p><p>Designation:%s</p>')%(visa_obj.name_of_director,visa_obj.director_cinnumber,visa_obj.company_name_director,visa_obj.designation_director)
						body = MIMEText(text, _subtype='html')
						msg.attach(body)
						server.sendmail(fromaddr, toaddr, msg.as_string())
		server.quit()
		return True

		# email_template_obj = self.pool.get('email.template')
		# template_ids = email_template_obj.search(cr, uid, [('model', '=','purchase.order')],context=context)[0]
		# if template_ids:
			# values = email_template_obj.generate_email(cr, uid, template_ids, ids, context=context)
			# values['subject'] = 'Test Mail' 
			# values['email_to'] ='venugopal@techanipr.com'
			# values['body_html'] = ''
			# values['body'] = ''
			# values['res_id'] = False
			# mail_mail_obj = self.pool.get('mail.mail')
			# msg_id = mail_mail_obj.create(cr, uid, values, context=context)
			# email_template_obj.send(cr, uid, [msg_id], template_ids,context=context) 
		# return True
	
		# ir_model_data = self.pool.get('ir.model.data')
		# try:
			# template_id = ir_model_data.get_object_reference(cr, uid, 'purchase', 'email_template_edi_purchase')[1]
		# except ValueError:
			# template_id = False
		# try:
			# compose_form_id = ir_model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
		# except ValueError:
			# compose_form_id = False 
		# ctx = dict(context)
		# ctx.update({
			# 'default_model': 'client.investment.risk.profile',
			# 'default_res_id': ids[0],
			# 'default_use_template': bool(template_id),
			# 'default_template_id': template_id,
			# 'default_composition_mode': 'comment',
		# })
		# return {
			# 'type': 'ir.actions.act_window',
			# 'view_type': 'form',
			# 'view_mode': 'form',
			# 'res_model': 'mail.compose.message',
			# 'views': [(compose_form_id, 'form')],
			# 'view_id': compose_form_id,
			# 'target': 'new',
			# 'context': ctx,
			# }

client_investment_risk_profile()

		