from openerp.osv import fields, osv
class hr_custom_joining_date(osv.osv):

	_inherit = "hr.employee"
	_columns = {

	'date_of_joining':fields.date('Date of Joining'),

	}

hr_custom_joining_date()
