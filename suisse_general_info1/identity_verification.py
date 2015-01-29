from openerp.osv import fields, osv
class identity_verification(osv.osv):
	_name="verify.identity"
	_columns={
	'ac_no':fields.char('Account No:'),
	'company_name':fields.char('Name of the contracting partner/Company'),
	'complete_addr':fields.text('Complete address'),
	'contracting_partneris_beneficial_owner':fields.boolean(''),
	'beneficial_owner_assets_concerned':fields.boolean(''),
	'fullname':fields.char('Full name'),
	'address_domicile':fields.char('address/domicile'),
	'country':fields.many2one('res.country','Country'),
	'place':fields.char('Place'),
	'date':fields.date('Date'),
	'sign':fields.char('Signature')
	}

identity_verification()