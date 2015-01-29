from openerp.osv import osv ,fields
from openerp.tools.translate import _
class test_wizard(osv.osv):
	_name = 'test.wizard'
	_description = "My 1st wizard"
	_columns = {
		'empname' : fields.char('Name',size=50),
		'empsalary' : fields.char('Salary',size=50),
		'empdept' : fields.char('Department',size=50),
		'address' : fields.text('Address',size=140),
	}
	def connect_anotherobj(self,cr,uid,ids,context=None):
		return {
					'type': 'ir.actions.act_window',
					'res_model': 'test2.wizard',
					'view_mode': 'form',
					'view_type': 'form',
					'res_id': False,
					'views': [(False, 'form')],
					'name' : _('Department Info'),
					'nodestroy': True,
					'target': 'new',
					 }
	
	def save(self,cr,uid,ids,context=None):
		data=self.read(cr,uid,ids)[0]
		create = self.pool.get('my.company').write(cr,uid,context['active_id'],{'emp_id': [[0, False, {'empdept': data['empdept'], 'empname': data['empname'], 'empsalary': data['empsalary']}]]},context=None)
		return True

test_wizard()
class test2_wizard(osv.osv):
	_name ='test2.wizard'
	_description = "my 2nd wizard"
	_columns = {
		'department' : fields.char('Department Name',size=50),
		'strength' : fields.char('Strength of depart',size=50),
		'deptaddress' : fields.char('DeptAddress',size=50),
	}
	def save_details(self,cr,uid,ids,context=None):
		print context
		data = self.read(cr, uid, ids)[0]
		print data
		if data['strength'] == '0':
			raise osv.except_osv(_('Warning!'), _('strength always greater than 0 !!'))
		return True
test2_wizard()
class test3_wizard(osv.osv):
	_name='test3.wizard'
	_description = " test 3rd object in wizard"
	_columns = {
		'name1' : fields.char('Name1',size=40),
		'name2' : fields.char('Name2',size=40),
	}
test3_wizard()