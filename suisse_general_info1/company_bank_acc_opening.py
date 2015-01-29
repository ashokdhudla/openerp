from openerp.osv import fields, osv
from openerp.tools.translate import _

class bank_account_opening_company(osv.osv):
	_name = 'bank.account.opening.company'
	_description = 'Bank Opening Form'
	
	_columns ={
		#Section B.1
		'name':fields.char('Description',select=True),
		'bank_kyc_name': fields.char('Name/Company name of the Financial intermediary',size=200),
		'name_of_company':fields.char('Name of the company',size=200,select=True),
		'street_one': fields.char('Street', size=128),
		'street2_one': fields.char('Street2', size=128),
		'zip_one': fields.char('PostCode', change_default=True, size=24),
		'city_one': fields.char('City', size=128),
		'state_id_one': fields.many2one("res.country.state", 'State'),
		'country_id_one': fields.many2one('res.country', 'Country of domicile'),
		'date_of_foundation':fields.date('Date of foundation', select=True),
		'user_id': fields.many2one('res.users', 'Created by', readonly=True, track_visibility='onchange'),
		#Section B.2
		'title':fields.char('Title',select=True),
		'first_name':fields.char('Surname/First name',select=True),
		'street_two': fields.char('Street', size=128),
		'street2_two': fields.char('Street2', size=128),
		'zip_two': fields.char('PostCode', change_default=True, size=24),
		'city_two': fields.char('City', size=128),
		'state_id_two': fields.many2one("res.country.state", 'State'),
	       	'country_id_two': fields.many2one('res.country', 'Country of domicile'),
		'nationality': fields.many2one('res.country', 'Nationality'),
        	'date_of_birth':fields.date('Date of Birth', select=True),
		'relationship_account':fields.text(''),
		#Section B.3
		'desc_of_financial_intermediary':fields.text(''),
		#Section C.1
		'marital_single':fields.boolean('Single'),
		'marital_married':fields.boolean('Married'),
		'marital_divorced':fields.boolean('Divorced'),
		'marital_separated':fields.boolean('Separated'),
		'marital_widowed':fields.boolean('Widowed'),
		'marital_unknown':fields.boolean('Unknown'),
		'name_of_spouse':fields.char('Name of spouse/partner'),
		'spouse_date':fields.date('Date of Birth',select=True),
		'yes_one':fields.boolean('Yes'),
		'no_one':fields.boolean('NO'),
		'yes_two':fields.boolean('Yes'),
		'no_two':fields.boolean('NO'),
		'personal_background':fields.one2many('bank.form.personal.background','children_id','Personal Details'),
		'info_sibling':fields.text(''),
		'note':fields.text(''),
		'c2_self_employed':fields.boolean('Self-employed'),
		'c2_employed':fields.boolean('Employed'),
		'c2_retired':fields.boolean('Retired'),
		'c2_student':fields.boolean('Student'),
		'c2_not_gain_employed':fields.boolean('Not gainfully employed'),
		'c2_other':fields.boolean('Other'),
		'c2_occupation_desc':fields.text('Client current/previous occcupation'),
		'c3_public_fun_Y':fields.boolean('Yes'),
		'c3_public_fun_N':fields.boolean('No'),
		'c3_politics':fields.boolean('Politics'),
		'c3_church':fields.boolean('Church'),
		'c3_armed_forces':fields.boolean('Armed forces'),
		'c3_aristrocracy':fields.boolean('Aristrocracy'),
		'c3_other':fields.boolean('Other'),
		'c3_details':fields.text(''),
		'c4_other_keyinfo':fields.text('Other key Info about the beneficial owner'),
		'd1_assets_value':fields.float('Current assets (total value)'),
		'd1_bank_deposits':fields.float('Bank deposits'),
		'd1_securities':fields.float('Securities'),
		'd1_stakes':fields.float('Stakes'),
		'd1_collections':fields.float('Collections'),
		'd1_life_insurance':fields.float('Life insurance'),
		'd1_realestate':fields.float('Real estate'),
		'd1_asset_other':fields.float('Other'),
		'd1_assets_details':fields.char('(Please specify)'),
		'd1_ubs_assets':fields.float('Thereof held by UBS'),
		'd1_assests_deposited_6to9mnths':fields.float('Total assets expected to be deposited with UBS in six to nine months'),
		'd1_majorstakes':fields.char('Major stakes(e.g.in companies)'),
		'd1_income_situation':fields.float('Income situation (estimate)'),
		'd1_income_sources':fields.char('Sources (e.g.salary,income from securities)'),
		'd1_total_currentdebts':fields.float('Total current debts'),
		'd1_loans':fields.float('Loans'),
		'd1_mortgages':fields.float('Mortgages'),
		'd1_other':fields.float('Other'),
		'd1_other_details':fields.char('(please provide details)'),
		'd2_assets_acquire_desc':fields.text('How beneficial owner acquire his/her assets'),
		'd2_gift_inheritance':fields.boolean('Gift/inheritance'),
		'd2_company_sale':fields.boolean('Sale of company'),
		'd2_income_salary':fields.boolean('Income/salary'),
		'd2_sale_proceeds':fields.boolean('Proceeds from sales'),
		'd2_sale_realestate':fields.boolean('Sale of real estate'),
		'd2_asset_source_other':fields.boolean('Other'),
		'd2_details_assets':fields.text('In each case please provide details'),
		'd2_bank_transfer':fields.boolean('Bank transfer'),
		'd2_security_delivery':fields.boolean('Delivery of securities'),
		'd2_cash_deposit':fields.boolean('Cash deposit'),
		'd2_partial_delivery':fields.boolean('Partial delivery'),
		'd2_deliver_asset_other':fields.boolean('Other'),
		'd2_details_assets_delivery':fields.text('If other provide details'),
		'd2_name':fields.char('Name (e.g.of bank)'),
		'd2_location': fields.many2one("res.country.state", 'Location'),
		'd2_country':fields.many2one('res.country', 'Country'),
		'f_place':fields.char('Place'),
		'f_date':fields.date('Date'),
		'f_sign':fields.char('Signature')
		
	}
	_defaults={
		'name':'Company Bank Opening Form',
	}
	_order = 'bank_kyc_name'
bank_account_opening_company()

class  bank_form_personal_background(osv.osv):
	_columns = {
		'name_of_children':fields.char('Name(s) of Children'),
		'children_occupation':fields.char('Occupation', change_default=True),
		'children_dof':fields.date('Date of Birth', change_default=True),
		'children_id':fields.many2one('bank.account.opening.company','Children', select=True, ondelete='cascade'),
	}

	
	_name = 'bank.form.personal.background'
	_description = 'Personal Background Children'

bank_form_personal_background()
