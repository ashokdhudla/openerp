from openerp.osv import fields, osv

class company_expense_details(osv.osv):

	_inherit = 'hr.expense.expense'

	_columns = {
		'company_expense':fields.boolean('Company Expense'),
		'state_id':fields.many2one('res.country.state','Location'),
	}


	def onchange_company_expense(self,cr,uid,ids,company_expense,context=None):
		res = {}
		if company_expense==True:
			emp_id = self.pool.get('hr.employee').search(cr,uid,[('name_related','=','Celina Trading LLc.')])
			if emp_id:
				res = {'value':{'employee_id':emp_id[0]}}
			return res
		else:
			ids = self.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)])
			if ids:
				res = {'value':{'employee_id':ids[0]}}
			return res
		return True

company_expense_details()