from openerp.osv import fields, osv
class lead_import_fields(osv.osv):
	_inherit = "crm.lead"
	_columns = {
		'firstname':fields.char('Firstname'),
		'lastname':fields.char('Lastname'),
		'lead_type': fields.many2one('crm.case.categ', 'Lead Type',required=True),
		}
		
	def create(self,cr,uid,vals,context=None):
		if 'name' not in vals:
			vals.update({'name':'Lead Subjects'})
		else:
			vals.update({'name':vals['name']})
		
		return super(lead_import_fields,self).create(cr,uid,vals,context=context)
	
lead_import_fields()