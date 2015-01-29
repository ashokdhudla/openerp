from openerp.osv import osv,fields
from openerp.tools.translate import _

class my_company(osv.osv):
	def total_cal(self, cr, uid, ids, field_name, arg, context=None):
		res = {}
		for fields in self.browse(cr, uid, ids, context=context):
			res[fields.id] = fields.exp3+fields.exp4+fields.totalexpenditure
		return res
	_name="my.company"
	_description = "Test Desc"
	_inherit = ['mail.thread']
	_columns = {
		# "company_name" : fields.char('Company name',size=50,required=True,translate=True),
		"name_company" : fields.char('Company name',size=50,required=True,translate=True),
		"company_config" : fields.many2one('company.info',string="Company name"),
		"tag_line_company" : fields.char('Company Tag Line',size=100,required=False),
		"state" : fields.selection([('draft','Draft'),('confirmed','Confirmed')],'State'),
		"image" : fields.binary("Image",help="This is the stored image for company"),
		"employees" : fields.many2one("res.partner",'Employee',required=True),
		# "active" : fields.boolean("Active"),
		'button_hide': fields.boolean('Hide button'),
		"company_street" : fields.char("Street",size=100,required=True),
		"company_city" : fields.char('City',size=50,required=True),
		"pincode" : fields.integer('Pincode',help="Company Area Pincode"),
		"country" : fields.many2one('res.country','Country'),
		"turnover" : fields.float('Turnover',digits=(10,2)),
		"development" : fields.boolean('Developement'),
		"service" : fields.boolean('Service'),
		"publtd" : fields.boolean('Private Limited Company'),
		"privateltd" : fields.boolean('Public Limited Company'),
		'expenditure1' : fields.integer('Expenditure1',size=20),
		'expenditure2' : fields.integer('Expenditure2',size=20),
		'totalexpenditure' : fields.float('TotalExpenditure',size=20),
		'exp3' : fields.integer('Expenditure3',size=20),
		'exp4' : fields.integer('Expenditure4',size=20),
		'total' : fields.function(total_cal,string='total',type='float'),
		'emp_id' : fields.one2many('emp.info','emp_data'),
		'states' : fields.selection([
			('first_state','First State'),
			('middle_state','Middle State'),
			('final_state','Final State'),
			],'States',readonly=True,track_visibility='onchange'),
		# 'employees_id': fields.many2many('hr.employee', 'mycompany_emp_rel', 'mycompany_id', 'emp_data', 'Associated Employees'),
	}
	def _default_country(self,cr,uid,context=None):
		country = self.pool.get('res.country').search(cr,uid,[('code','=','IN')],context=None)
		# print country[0]
		return country[0]

	def _default_partner(self,cr,uid,context=None):
		partner = self.pool.get('res.partner').search(cr,uid,[('name','=','ashok')],context=None)
		# print partner
		# return partner[0]
		return True
	def create(self, cr, uid, vals, context=None):
		print "helloooooo im in create method..............."
		if vals.get('tag_line_company','/')=='/':
			vals['tag_line_company'] = self.pool.get('ir.sequence').get(cr, uid, 'my.company') or '/'
			print "my company create"
		return super(my_company, self).create(cr, uid, vals, context=context)
		# employee_id = super(my_company, self).create(cr, uid, data, context=context)
		# try:
		# 	(model, mail_group_id) = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'mail', 'group_all_employees')
		# 	employee = self.browse(cr, uid, employee_id, context=context)
		# 	# print "hello your in create method"
		# 	self.pool.get('mail.group').message_post(cr, uid, [mail_group_id],
		# 		body=_('Welcome to %s! Please help him/her take the first steps with OpenERP helooooooooooooooo!') % (employee.company_name),
		# 		subtype='mail.mt_comment', context=context)
			
		# except:
		# 	pass # group deleted: do not push a message
		# return employee_id
		# if context is None: context = {}
  #       # Prevent double project creation when 'use_tasks' is checked!
  #       context = dict(context, project_creation_in_progress=True)
  #       mail_alias = self.pool.get('mail.alias')
  #       if not vals.get('alias_id') and vals.get('name', False):
  #           vals.pop('alias_name', None) # prevent errors during copy()
  #           alias_id = mail_alias.create_unique_alias(cr, uid,
  #                         # Using '+' allows using subaddressing for those who don't
  #                         # have a catchall domain setup.
  #                         {'alias_name': "project+"+short_name(vals['name'])},
  #                         model_name=vals.get('alias_model', 'my.company'),
  #                         context=context)
  #           vals['alias_id'] = alias_id
  #       if vals.get('type', False) not in ('template','contract'):
  #           vals['type'] = 'contract'
  #       project_id = super(my_company, self).create(cr, uid, vals, context)
  #       mail_alias.write(cr, uid, [vals['alias_id']], {'alias_defaults': {'project_id': project_id} }, context)
  #       return project_id
	# def create(self,cr,uid,vals,context=None):
	# 	print vals['company_name']
	# 	if vals['company_name'] == 'flumensoft':
	# 		raise osv.except_osv(_('Hello Flumensoft.'),_("This is experts den!") )
	# 	print vals
	# 	return super(my_company,self).create(cr,uid,vals,context=None)

	# def write(self,cr,uid,vals,context=None):
	# 	print vals
	# 	data=self.read(cr,uid,ids)[0]
	# 	print data
	# 	# res = super(my_company,self).read(cr,uid,ids,context=None)
	# 	# print res
	# 	if vals['company_name'] == 'flumensoft':
	# 		raise osv.except_osv(_('Hello Flumensoft.'),_("This is experts den!") )
	# 	return super(my_company,self).write(cr,uid,vals,context=None) 

	# def read(self,cr,uid,ids,context=None):
	# 	res = super(my_company,self).read(cr,uid,ids,context=None)
	# 	print res
	# 	return res
	_defaults = {
		# 'company_name' : 'Techanipr',
		'tag_line_company' : 'need good service approach techanipr ',
		'pincode' : 500084,
		'country' : _default_country,
		'employees' : _default_partner,
		'states' : 'first_state',
	}
	def company_change(self, cr, uid, ids, publtd,privateltd, context=None):
		vals = {}
		if publtd == True:
			vals.update({'privateltd':False})
		return {'value' : vals}
	def company_change1(self, cr, uid, ids, publtd,privateltd, context=None):
		val = {}
		if privateltd == True:
			val.update({'publtd':False})
		return {'value' : val}	

	def total_exp(self, cr, uid, ids, expenditure1, expenditure2, context=None):
		return {'value': {'totalexpenditure': expenditure1 + expenditure2}}

	def change_stage(self, cr, uid, ids,context=None):
		write=self.write(cr,uid,ids,{'states' : 'middle_state'},context=None)
		return True

	def done_stage(self, cr, uid, ids, context=None):
		write=self.write(cr,uid,ids,{'states': 'final_state'},context=None)
		return True

	def print_report(self, cr, uid, ids, context=None):
			'''
			This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
			'''
			assert len(ids) == 1, 'This option should only be used for a single id at a time'
			datas = {
					'model': 'my.company',
					'ids': ids,
					'form': self.read(cr, uid, ids[0], context=context),
				}
			return {'type': 'ir.actions.report.xml', 'report_name': 'my.company', 'datas': datas, 'nodestroy': True}

	def testing(self, cr, uid, ids, context=None):
			
			# obj1 = self.pool.get('res.partner').search(cr,uid,[('name','=','ashok')],context=None)
			# obj = self.pool.get('res.partner').search(cr,uid,[('id','!=',1)],context=None)
			# for name in self.pool.get('res.partner').browse(cr,uid,obj,context=None):
			# 	print name.name
			# 	print name.email
			# 	print name.display_name
			# obj = self.pool.get('res.partner').search(cr,uid,[('name','=','advaaz')],context=None)
			# obj1 = self.pool.get('res.partner').write(cr,uid,obj,{'name':'Techanipr'},context=None)
			# print obj1
			# create = self.pool.get('res.partner').create(cr,uid,{'name':'Hitechnologie','email': 'info@hitech.com'},context=None)
			# print create
			# read = self.pool.get('res.partner').read(cr,uid,[8],context=None),
			# print read
			# copy = self.pool.get('res.partner').copy(cr,uid,10,default=None,context=None)
			# print copy
			# copy = self.pool.get('res.partner').copy_data(cr,uid,8,default=None,context=None)
			# print copy
			# unlink = self.pool.get('res.partner').unlink(cr,uid,[11],context=None)
			# print unlink
			# default = self.pool.get('res.partner').fields_get(cr,uid,[10],context=None)
			# print default
			# print obj
			# for name in self.pool.get('res.users').browse(cr,uid,obj,context=None):
			# 	print name.password
			# 	print name.login
			# tids = self.pool.get('res.partner').create(cr,uid,{'name' : 'venugopa','street' : 'pmh','fax' : 'abcd'})
			# print tids
			# tids = self.pool.get('res.partner').write(cr,uid,[9],{'name' : 'aravind'})
			# print tids
			# tids = self.pool.get('res.partner').default_get(cr,uid,['vat'],context=None)
			# data = {}
			# data['vat'] = '123456'
			# print tids
			# cr.execute('select * from res_partner')
			# obj = cr.fetchall()
			# print obj
			# cr.execute('select * from res_partner where id=1')
			# obj= cr.fetchone()
			# print obj[1]
			# cr.execute('CREATE TABLE My_TABLE (ID INT Primary key NOT NULL,name Text,age int)')
			# fieldsget = self.pool.get('res.partner').fields_view_get(cr,uid,['name'],context=None)
			# print fieldsget
			name_get = self.pool.get('res.partner').name_get(cr,uid,ids,context=None)
			print name_get
			return True
			# return data

	# def write(self,cr,uid,ids,vals,context=None):
	# 	print vals
	# 	return super(my_company,self).write(cr,uid,ids,vals,context=None)

my_company()
class emp_details(osv.osv):
	_name = 'emp.info'
	_description = "Empolyee information"
	_columns= {
		'emp_data' : fields.many2one('my.company'),
		'empname' : fields.char('Emp Name',size=50),
		'empdept' : fields.char('Emp Dept',size=50),
		'empsalary' : fields.char('Emp salary',size=50),
	}
emp_details()
# class emp_department(osv.osv):
# 	_name = 'emp.dept'
# 	_description = 'Employee Dept'
# 	_columns = {
# 		'emp_data' : fields.many2one('emp.info'),
# 		'emp_addres' : fields.char('Employee Address',size=50),
# 	}
# emp_department()
