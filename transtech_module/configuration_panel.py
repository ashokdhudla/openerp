from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
import time
import pytz

class state_setup(osv.osv):

	_inherit="res.country.state"
	_columns = {
	'country_id': fields.many2one('res.country', 'Country',
            required=True,domain="[('code','=','AE')]"),
	}

	def _default_country(self, cr, uid, context=None):
		cid = self.pool.get('res.country').search(cr, uid, [('code', '=', 'AE')], context=context)
		return cid[0]

	_defaults = {
	'country_id':_default_country,
	}


state_setup()

class reason_code_setup(osv.osv):

	_name = 'reason.code'

	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
		default.update({
            'reason_code': self.pool.get('ir.sequence').get(cr, uid, 'reason.code'),
        })
		return super(reason_code_setup, self).copy(cr, uid, id, default, context=context)

	_columns = {
		'reason_code':fields.char("Code",size=60,readonly=True),
		'name':fields.char('Reason Code', size=240),
		
	}
	
	def create(self, cr, uid, vals, context=None):
		if vals.get('reason_code','/')== '/':
			vals['reason_code'] = self.pool.get('ir.sequence').get(cr, uid, 'reason.code') or '/'
		return super(reason_code_setup, self).create(cr, uid, vals, context=context)

reason_code_setup()

class remarks_category(osv.osv):

	_name = 'remarks.category'

	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
		default.update({
            'description': self.pool.get('ir.sequence').get(cr, uid, 'remarks.category'),
        })
		return super(remarks_category, self).copy(cr, uid, id, default, context=context)

	_columns = {
		'description':fields.char("Remark Category ID",size=200,readonly=True),
		'name':fields.char('Remark Description', required=True),
	}
	def create(self, cr, uid, vals, context=None):
		if vals.get('description','/')== '/':
			vals['description'] = self.pool.get('ir.sequence').get(cr, uid, 'remarks.category') or '/'
		return super(remarks_category, self).create(cr, uid, vals, context=context)

		

remarks_category()

class manage_group(osv.osv):

	_inherit="res.groups"

manage_group()


class manage_users(osv.osv):
	
	_inherit="res.users"

	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
		default.update({
            'tuser_id': self.pool.get('ir.sequence').get(cr, uid, 'res.users'),
        })
		return super(manage_users, self).copy(cr, uid, id, default, context=context)
        
	_columns ={
		'tuser_id':fields.char('User ID',readonly=True, size=64),
		'contact_num':fields.char('Contact Number',size=64),
		'joining_date':fields.date('Joining Date'),
		'Comments':fields.text('Comments'),
		'role':fields.char('Role',size=64),
		'survey_limit':fields.integer('Limit of Surveys'),
	}

	def create(self, cr, uid, vals, context=None):
		if 'teamleader' in vals or 'name_tl' in vals:
			if vals['teamleader'] == True and vals['name_tl'] == False:
				vals.update({'role':'Teamleader'})
			if vals['name_tl'] != False and vals['teamleader'] == False:
				vals.update({'role':'Surveyor'})
			if vals['teamleader'] == False and vals['name_tl'] == False:
				vals.update({'role':'Customer'})
			if vals['teamleader'] == True and vals['name_tl'] != False:
				raise osv.except_osv(_('You cannot select both "Is Team Leader??" and "TeamLeader" fields at a time.' ),_("Please select only one of them.") )

		if vals.get('tuser_id','/')== '/':
			vals['tuser_id'] = self.pool.get('ir.sequence').get(cr, uid, 'res.users') or '/'
		result = super(manage_users, self).create(cr, uid, vals, context=context)
		del_id = self.pool.get('res.groups').search(cr,uid,[('name','=','Employee')])
		cr.execute('DELETE from  res_groups_users_rel where uid = %s and gid = %s', (result, del_id[0]))
		return result

	def write(self, cr, uid, ids, vals, context=None):
		# print vals
		# if 'name' in vals or 'image' in vals:
		# 	user = self.browse(cr,uid,ids)
		# 	print user
		# 	if not user.role=='Teamleader' or user.role=='Surveyor':
		# 		raise osv.except_osv(_('You cannot change the details of customer from here.' ),_("Please edit it through Customer Details Menu.") )
		if 'teamleader' in vals:
			if vals['teamleader'] == True:
				vals.update({'role':'Teamleader'})
			else:
				vals.update({'role':'Surveyor'})
		if 'name_tl' in vals:
			if vals['name_tl'] != False:
				vals.update({'role':'Surveyor'})
			else:
				vals.update({'role':'Teamleader'})

		# if 'teamleader' not in vals and 'name_tl' not in vals:
		# 	vals.update({'role':'Customer'})
		
		if 'teamleader' in vals and 'name_tl' in vals:
			if vals['teamleader'] == True and vals['name_tl'] != False:
				raise osv.except_osv(_('You cannot select both "Is Team Leader??" and "TeamLeader" fields at a time.' ),_("Please select only one of them.") )
		return super(manage_users,self).write(cr,uid,ids,vals,context=None)


manage_users()


class set_tz(osv.osv):

	_inherit="res.partner"


	def _tz_get(self,cr,uid, context=None):
	    # put POSIX 'Etc/*' entries at the end to avoid confusing users - see bug 1086728
	    return [(tz,tz) for tz in sorted(pytz.all_timezones, key=lambda tz: tz if not tz.startswith('Etc/') else '_')]

	_columns={
	'tz': fields.selection(_tz_get,'Timezone', size=64),
	}


	# def _default_tz(self, cr, uid, context=None):
	# 	u_id = self.pool.get('res.users').browse(cr,uid,uid)
	# 	part_id = self.search
	_defaults={
	'tz':'Asia/Dubai',
	}