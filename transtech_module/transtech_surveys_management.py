from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
import time
from dateutil.relativedelta import relativedelta
from openerp import SUPERUSER_ID
class atm_surverys_management(osv.osv):
	_name="atm.surverys.management"

	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
		default.update({
            'name': self.pool.get('ir.sequence').get(cr, uid, 'atm.surverys.management'),
        })
		return super(atm_surverys_management, self).copy(cr, uid, id, default, context=context)

	_columns={
		'name':fields.char('Task ID', readonly=True),
        'task_month':fields.selection([
		    ('jan','Janauray'),
		    ('feb', 'February'),
		    ('mar', 'March'),
		    ('apr', 'April'),
		    ('may', 'May'),
		    ('june','June'),
		    ('jul', 'July'),
		    ('aug', 'August'),
		    ('sep', 'September'),
		    ('oct', 'October'),
		    ('nov', 'November'),
		    ('dec', 'December'),
		    ], 'Month'),
		'customer':fields.many2one('customer.info','Customer',size=64,required=True),
		'state':fields.many2one('res.country.state','State',required=True,domain="[('country_id','=',country)]"),
		'atm':fields.many2one('atm.info','ATM',domain="[('customer','=',customer),('state_id','=',state)]"),
		'country':fields.many2one('res.country','Country', domain="[('code','=','AE')]",required=True),
		'surveyor':fields.many2one('res.users','Surveyor', domain="[('name_tl','!=',False)]",required=True),
		'visit_time':fields.datetime('Visit Date And Time',required=True),
		'additional_info':fields.text('Additional instructions'),
		'status': fields.selection([
		    ('assigned','Assigned'),
		    ('pending', 'Pending'),
		    ('cancel', 'Cancelled'),
		    ('progress', 'Progress'),
		    ('waitnig_approve','Waiting for Approval'),
		    ('done', 'Done'),
		    ], 'Status',readonly=True, track_visibility='always'),
		'bulk_insert':fields.boolean('Bulk Insert'),
		'nos':fields.integer('Number of records for Bulk Insert '),
		'remarks_id':fields.many2one('remarks.category', 'Remarks Category'),
		'remarks':fields.text('Remarks'),
		'act_visit_time':fields.datetime('Actual Date Time'),
		'assigned_by':fields.many2one('res.users','Assigned By' ,readonly=True),
		'visit_type': fields.selection([
		    ('daily','Daily'),
		    ('weekly', 'Weekly'),
		    ('monthly', 'Monthly'),
		    ], 'Visit Type'),
		'next_visit':fields.datetime('Next Visit',readonly=True),
		'visit_shift':fields.selection([('day','Day'),('night','Night')] ,'Visit Shift',required=True),
	}
	_order = "name desc"
	def _default_country(self, cr, uid, context=None):
		cid = self.pool.get('res.country').search(cr, uid, [('code', '=', 'AE')], context=context)
		return cid[0]

	_defaults = {
	'assigned_by': lambda obj, cr, uid, ctx=None: uid,
	'status':'assigned',
	'visit_shift':'day',
	'country':_default_country,
	}

	def status_done(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'done'},context=context)
		return True

	def status_cancel(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'cancel'},context=context)
		return True

	def create(self,cr,uid,vals,context=None):
		if vals['surveyor'] != False:
			u_ids = self.pool.get('res.users').search(cr,uid,[('id','=',vals['surveyor'])])
			u_obj = self.pool.get('res.users').browse(cr,uid,u_ids[0])
			today =  str(datetime.datetime.now()).split(' ')[0]
			t_ids = self.search(cr,uid,[('surveyor','=',vals['surveyor'])])
			counter = 0
			for i in self.browse(cr,uid,t_ids):
				if i.visit_time != False:
					if i.visit_time.split(' ')[0] == today:
						counter = counter+1
			if counter == u_obj.survey_limit:
				raise osv.except_osv(_('The Survey Limit of this Surveyor has been exceeded.'),_("Please assign tasks tomorrow for this Surveyor !") )
		if vals['bulk_insert'] == True and vals['nos'] > 0:
			if vals['visit_type'] == 'daily':
				visit_date = datetime.datetime.strptime(vals['visit_time'], "%Y-%m-%d %H:%M:%S")
				vals['next_visit']  = visit_date + datetime.timedelta(days=1)
			if vals['visit_type'] == 'weekly':
				visit_date = datetime.datetime.strptime(vals['visit_time'], "%Y-%m-%d %H:%M:%S")
				vals['next_visit']  = visit_date + datetime.timedelta(days=7)
			if vals['visit_type'] == 'monthly':
				visit_date = datetime.datetime.strptime(vals['visit_time'], "%Y-%m-%d %H:%M:%S")
				vals['next_visit'] = visit_date+ relativedelta(months=1)

		if vals.get('name','/') == '/': 
			vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'atm.surverys.management') or '/'
		return super(atm_surverys_management, self).create(cr, uid, vals, context=context)
		

	def create_task(self,cr,uid,context=None):
		today =  str(datetime.datetime.now()).split(' ')[0]
		ids1 = self.search(cr,uid,[('next_visit','!=',False)])
		task_list = self.browse(cr,uid,ids1,context=None)
		print today
		print datetime.datetime.today().weekday()
		vals = {}
		for i in task_list:
			print i.next_visit.split(' ')[0]
			if i.next_visit.split(' ')[0] == today and i.nos > 0:
				
				# print i.status
				if i.status == 'assigned' or i.status == 'progress' or i.status == 'pending' or i.status== 'done':
					print i.id
					vals = {'task_month':i.task_month,'customer':i.customer.id, 'atm':i.atm.id, 'country':i.country.id, 'state':i.state.id, 'surveyor':i.surveyor.id,'visit_time':i.next_visit,'additional_info':i.additional_info,'bulk_insert':i.bulk_insert,'nos':i.nos, 'visit_type':i.visit_type,'act_visit_time':i.act_visit_time,'nos':i.nos-1}
					if datetime.datetime.today().weekday() != 4:
						self.pool.get('atm.surverys.management').create(cr,uid,vals,context=None)
					else:
						return True
		return True

	def change_task_status(self,cr,uid,context=None):
		today =  str(datetime.datetime.now()).split()[0]
		all_tasks = self.search(cr,uid,[('visit_time','!=',False)])
		task_list1 = self.browse(cr,uid,all_tasks,context=None)
		for obj in task_list1:
			if obj.status == 'assigned' or obj.status == 'progress' or obj.status == 'pending':
				if obj.visit_time.split()[0] == today:
					self.pool.get('atm.surverys.management').write(cr,uid,obj.id,{'status':'progress'},context=None)
				elif obj.visit_time.split()[0] < today:
					self.pool.get('atm.surverys.management').write(cr,uid,obj.id,{'status':'pending'},context=None)
				else:
					self.pool.get('atm.surverys.management').write(cr,uid,obj.id,{'status':'assigned'},context=None)

		return True

	def write(self,cr,uid,ids,vals,context=None):
		if isinstance(ids, (int, long)):
			ids = [ids]

		result = super(atm_surverys_management,self).write(cr,uid,ids,vals,context=None)
		lst = self.browse(cr,uid,ids)
		for obj in lst:
			if obj.nos > 0:
				if obj.visit_type == 'daily':
					visit_date = datetime.datetime.strptime(obj.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit']  = visit_date + datetime.timedelta(days=1)
				if obj.visit_type == 'weekly':
					visit_date = datetime.datetime.strptime(obj.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit']  = visit_date + datetime.timedelta(days=7)
				if obj.visit_type == 'monthly':
					visit_date = datetime.datetime.strptime(obj.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(months=1)
				super(atm_surverys_management,self).write(cr,uid,ids,vals,context=None)

		return True

	def unlink(self, cr, uid, ids, context=None):
        	prod_obj = self.pool.get('atm.surverys.management').browse(cr,uid,ids[0])
		if prod_obj.status in ('progress','pending','done'):
			raise osv.except_osv(_('Invalid Action!'), _("You can't delete a task which is either in 'Pending state' or in 'Progress state' or in 'Done state '"))
        	
        	return super(atm_surverys_management, self).unlink(cr, uid, ids, context=context)

	# def search(self,cr,uid,args,context=None):
	# 	print uid
	# 	print 'php vals',args

	# 	res =  super(atm_surverys_management,self).search(cr,uid,args)
	# 	#print res
	# 	return res

atm_surverys_management()

class is_teamleader(osv.osv):
	_inherit = "res.users"
	_columns = {
	'teamleader':fields.boolean('Is Team Leader??'),
	'name_tl':fields.many2one('res.users','Team Leader', domain="[('role','!=','Customer'),('role','!=','Surveyor')]"),
	'password': fields.char('Password', size=64,
            help="Keep empty if you don't want the user to be able to connect on the system."),
	}

is_teamleader()

class res_users(osv.Model):
    """ Update of res.users class
        - add a preference about sending emails about notifications
        - make a new user follow itself
        - add a welcome message
    """
    _name = 'res.users'
    _inherit = ['res.users']
    _inherits = {'mail.alias': 'alias_id'}

    def create(self, cr, uid, data, context=None):
        # create default alias same as the login
        if not data.get('login', False):
            raise osv.except_osv(_('Invalid Action!'), _('You may not create a user. To create new users, you should use the "User Management > Users" menu.'))

        mail_alias = self.pool.get('mail.alias')
        alias_id = mail_alias.create_unique_alias(cr, uid, {'alias_name': data['login']}, model_name=self._name, context=context)
        data['alias_id'] = alias_id
        data.pop('alias_name', None)  # prevent errors during copy()

        # create user
        user_id = super(res_users, self).create(cr, uid, data, context=context)
        user = self.browse(cr, uid, user_id, context=context)
        # alias
        mail_alias.write(cr, SUPERUSER_ID, [alias_id], {"alias_force_thread_id": user_id}, context)
        # create a welcome message
        self._create_welcome_message(cr, uid, user, context=context)
        return user_id

    def _create_welcome_message(self, cr, uid, user, context=None):
        if not self.has_group(cr, uid, 'base.group_user'):
            return False
        company_name = user.company_id.name if user.company_id else ''
        body = _('%s has joined the %s network.') % (user.name, company_name)
        # TODO change SUPERUSER_ID into user.id but catch errors
        return self.pool.get('res.partner').message_post(cr, SUPERUSER_ID, [user.partner_id.id],
            body=body, context=context)
res_users()



