from openerp.osv import fields, osv

class sale_person_designation(osv.osv):
	_inherit="res.users"
	_columns={
	'function':fields.char('Designation', size=100),
	}
sale_person_designation()